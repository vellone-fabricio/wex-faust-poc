import faust

app = faust.App('mytest-app', broker="kafka://localhost:9093")

test_topic = app.topic("test-topic", key_type=str, value_type=str, value_serializer="raw")

@app.task
async def hello_when_starting():
    print("Application started succesfully!")

@app.timer(interval=1)
async def publishing_random_to_a_topic():
    await test_topic.send(key="Me", value="Hey hey")

@app.agent(test_topic)
async def order(stream):
    async for key, value in stream.items():
        print(f"This data was received: {value} with key: {key}")
