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
from psycopg import connect

DATABASE_URL = os.getenv("DATABASE_URL")


@app.get("/db-init")
def db_init():
    sql = """
    CREATE TABLE IF NOT EXISTS matches (
        id BIGSERIAL PRIMARY KEY,
        api_fixture_id BIGINT UNIQUE NOT NULL,
        league_id INTEGER,
        league_name VARCHAR(150),
        season INTEGER,
        home_team_id INTEGER,
        home_team_name VARCHAR(150),
        away_team_id INTEGER,
        away_team_name VARCHAR(150),
        match_date TIMESTAMPTZ,
        status VARCHAR(50),
        home_goals INTEGER,
        away_goals INTEGER,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );
    """

    with connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)

    return {
        "status": "ok",
        "message": "Tabela matches criada/verificada"
    }

