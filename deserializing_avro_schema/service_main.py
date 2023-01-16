from fastapi import FastAPI

app = FastAPI()

in_memorian_db = {
    "relc-ygyr4jz7kh55555": "org-12312412412"
}

@app.on_event("start")
async def on_start():
    print("Starting application!")

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/{id}")
async def get_by_id(id: str):
    fetched_id = in_memorian_db.get(id, None)

    return fetched_id
