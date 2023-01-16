import json

import requests


def main():
    schemas = [
        {
            "name": "email",
            "namespace": "notifications.queue",
            "type": "record",
            "fields": [
                {
                    "name": "notification_id",
                    "type": ["null", "string"],
                },
                {"name": "relationship_account_id", "type": "string"},
                {"name": "source_system", "type": ["null", "string"]},
                {"name": "organization_id", "type": ["null", "string"]},
                {"name": "api_key", "type": "string"},
                {"name": "from_address", "type": "string"},
                {
                    "name": "to",
                    "type": {
                        "type": "array",
                        "items": "string",
                        "default": [],
                    },
                },
                {
                    "name": "cc",
                    "type": {
                        "type": "array",
                        "items": "string",
                        "default": [],
                    },
                },
                {
                    "name": "bcc",
                    "type": {
                        "type": "array",
                        "items": "string",
                        "default": [],
                    },
                },
                {
                    "name": "attachments",
                    "type": [
                        "null",
                        {
                            "type": "array",
                            "items": {
                                "name": "file",
                                "type": "record",
                                "fields": [
                                    {
                                        "name": "s3_bucket_name",
                                        "type": "string",
                                    },
                                    {"name": "s3_key_name", "type": "string"},
                                    {"name": "file_name", "type": "string"},
                                ],
                            },
                        },
                    ],
                },
                {
                    "name": "content",
                    "type": {
                        "type": "record",
                        "name": "Content",
                        "fields": [
                            {"name": "html_body", "type": "string"},
                            {"name": "text_body", "type": "string"},
                        ],
                    },
                },
            ],
        }
    ]

    headers = {"content-type": "application/vnd.schemaregistry.v1+json"}

    schema_types = ["email"]
    for schema, schema_type in zip(schemas, schema_types):
        data = json.dumps({"schema": json.dumps(schema)})

        response = requests.post(
            (
                "http://faust-poc-karapace-registry:8081/subjects/"
                "my-topic."
                f"{schema_type}/versions"
            ),
            headers=headers,
            data=data,
        )

        response.raise_for_status()
        response_data = response.json()
        id = response_data["id"]

        print(
            f"my-topic.{schema_type} "
            "schema saved in local Karapace Registry."
            f" Schema ID: {id}."
        )


if __name__ == "__main__":
    main()
