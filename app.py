import os
from fastapi import FastAPI

app = FastAPI()

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
