import io
import json
import faust
from fastavro import parse_schema, schemaless_reader
from fastavro.types import Schema
import requests

class AvroSchemaDecoder(faust.Schema):
  
    """An extension of Faust Schema class. The class is used by Faust when
    creating streams from Kafka topics. The decoder deserializes each message 
    according to the AVRO schema injected in each message's header.
    """
    def _fetch_schema(
        self
    ) -> Schema:
        try:
            response = requests.get(
                "http://faust-poc-karapace-registry:8081"
                f"/subjects/my-topic.email/versions/latest",
            )
            response.raise_for_status()

            response_data = response.json()
            schema = json.loads(response_data["schema"])
            parsed_schema = parse_schema(schema)


            return parsed_schema
        
        except Exception as err:
            raise Exception(
                f"{err}"
            )

    def __fast_avro_decode(self, schema, encoded_message):
        stringio = io.BytesIO(encoded_message)
        return schemaless_reader(stringio, schema)

    def loads_value(self, app, message, *, loads=None, serializer=None):
        # headers = dict(message.headers)
        # avro_schema = fastavro.parse_schema(headers["wex.event_name"])
        schema = self._fetch_schema()
        return self.__fast_avro_decode(schema=schema, encoded_message=message.value)


    def loads_key(self, app, message, *, loads=None, serializer=None):
        return message.key

app = faust.App('deserialization-app', broker="faust-poc-kafka:9092")

my_table = app.Table("test-table", default=str, partitions=1)

test_topic = app.topic(
    "my-topic",
    value_type=bytes,
    key_type=str,
    schema=AvroSchemaDecoder(),
    value_serializer="raw",
)

@app.task
async def hello_when_starting():
    print("Hello, application started succesfully!")


@app.agent(test_topic, concurrency=2)
async def order(stream):
    async for key, value in stream.items():
        parsed_key = key.decode("utf-8")
        print(f"This data was received: {value} with key: {parsed_key}")

        org_id = my_table[parsed_key]
        if org_id == '':
            print("Fetching data....")
            resp = requests.get(f"http://fastapi-test-service:8000/{parsed_key}")
            org_id = resp.json()
            print(org_id)

            print(f"Fetched new ID!: {org_id}")
            # # Saves data in the changelog topic
            my_table[parsed_key] = org_id
        else:
            print("Data was cached!")
        
        value["organization_id"] = org_id

        print(f"---Enriched data: {value}")


if __name__ == "__main__":
    app.main()