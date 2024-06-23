from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def initial():
    return {"message":"it works"}