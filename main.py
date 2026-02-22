from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

ALLOWED_NUMBER = "918948329366"
EVOLUTION_URL = os.getenv("EVOLUTION_URL")
API_KEY = os.getenv("AUTHENTICATION_API_KEY")
AWS_INVOKE_URL = os.getenv("AWS_INVOKE_URL")
INSTANCE = "primary"

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("Incoming:", data)

    try:
        message = data["data"]["message"]["conversation"]
        number = data["data"]["key"]["remoteJid"]

        # Extract numeric part
        sender_number = number.split("@")[0]

        # 🔒 Restrict access
        if sender_number != ALLOWED_NUMBER:
            print(f"Blocked message from: {sender_number}")
            return {"status": "ignored"}

        response = requests.post(
            AWS_INVOKE_URL,
            json={
                "user_id": number,
                "message": message
            },
            timeout=10
        )

        reply = response.json()["reply"]

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