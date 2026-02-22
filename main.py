from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

EVOLUTION_URL = os.getenv("EVOLUTION_URL")
API_KEY = os.getenv("AUTHENTICATION_API_KEY")
INSTANCE = "primary"

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("Incoming:", data)

    try:
        message = data["data"]["message"]["conversation"]
        number = data["data"]["key"]["remoteJid"]

        reply = f"You said: {message}"

        requests.post(
            f"{EVOLUTION_URL}/message/sendText/{INSTANCE}",
            headers={"apikey": API_KEY},
            json={
                "number": number,
                "text": reply
            }
        )

    except Exception as e:
        print("Error:", e)

    return {"status": "ok"}