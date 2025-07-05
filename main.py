from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Schema
class ChatRequest(BaseModel):
    message: str

# API Route
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_message = request.message
    payload = {
        "contents": [
            {"parts": [{"text": f"You are Bhushan Chatbot, a helpful assistant. User says: {user_message}"}]}
        ]
    }
    try:
        response = requests.post(GEMINI_URL, json=payload)
        data = response.json()
        bot_reply = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I couldn't understand that.")
    except Exception as e:
        bot_reply = f"Error: {str(e)}"
    return {"reply": bot_reply}

# Run locally
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
