from fastapi import FastAPI

# python -m uvicorn books:app --reload

app = FastAPI()

@app.get("/")
async def first_call():
    return {
        "Dedeius":"Hello!"
    }