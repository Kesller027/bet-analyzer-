import os
import httpx
from fastapi import FastAPI

app = FastAPI()

API_KEY = os.getenv("API_FOOTBALL_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


@app.get("/")
def home():
    return {
        "status": "online",
        "service": "bet-analyzer"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


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


@app.get("/telegram-test")
async def telegram_test():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": "-867855514",
        "text": "🤖 Bet Analyzer: teste do Telegram funcionando!"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data)

    return {
        "status_code": response.status_code,
        "telegram_response": response.json()
    }
