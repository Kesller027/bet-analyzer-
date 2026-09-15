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
    @app.get("/collect-next")
async def collect_next():
    url = "https://v3.football.api-sports.io/fixtures?next=1"
    headers = {"x-apisports-key": API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    data = response.json()

    if response.status_code != 200:
        return {
            "status": "error",
            "api_response": data
        }

    fixture = data["response"][0]

    f = fixture["fixture"]
    league = fixture["league"]
    teams = fixture["teams"]
    goals = fixture["goals"]

    sql = """
    INSERT INTO matches (
        api_fixture_id,
        league_id,
        league_name,
        season,
        home_team_id,
        home_team_name,
        away_team_id,
        away_team_name,
        match_date,
        status,
        home_goals,
        away_goals
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s
    )
    ON CONFLICT (api_fixture_id)
    DO UPDATE SET
        status = EXCLUDED.status,
        home_goals = EXCLUDED.home_goals,
        away_goals = EXCLUDED.away_goals,
        updated_at = NOW();
    """

    values = (
        f["id"],
        league["id"],
        league["name"],
        league["season"],
        teams["home"]["id"],
        teams["home"]["name"],
        teams["away"]["id"],
        teams["away"]["name"],
        f["date"],
        f["status"]["short"],
        goals["home"],
        goals["away"]
    )

    with connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, values)

    return {
        "status": "ok",
        "message": "Jogo real coletado e salvo no PostgreSQL",
        "fixture_id": f["id"],
        "league": league["name"],
        "home": teams["home"]["name"],
        "away": teams["away"]["name"],
        "date": f["date"]
    }

