import os
import httpx
from fastapi import FastAPI

app = FastAPI()

API_KEY = os.getenv("API_FOOTBALL_KEY")


@app.get("/")
def home():
    return {
        "status": "online",
        "service": "bet-analyzer"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/api-test")
async def api_test():
    url = "https://v3.football.api-sports.io/status"

    headers = {
        "x-apisports-key": API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    return {
        "status_code": response.status_code,
        "api_response": response.json()
    }
