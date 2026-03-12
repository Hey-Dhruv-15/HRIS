import os
import requests
from typing import Optional
from agent.local_agent import answer_question as local_answer

ADK_API_URL = os.environ.get("NHRIS_ADK_API_URL")
APP_NAME = os.environ.get("NHRIS_ADK_APP", "nhris_adk_agent")
USER_ID = os.environ.get("NHRIS_ADK_USER", "demo-user")
SESSION_ID = os.environ.get("NHRIS_ADK_SESSION", "demo-session")


def _ensure_session() -> None:
    if not ADK_API_URL:
        return
    url = f"{ADK_API_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID}"
    requests.post(url, timeout=10)


def ask_agent(prompt: str) -> Optional[str]:
    if not ADK_API_URL:
        return local_answer(prompt)
    try:
        _ensure_session()
        url = f"{ADK_API_URL}/run"
        payload = {
            "appName": APP_NAME,
            "userId": USER_ID,
            "sessionId": SESSION_ID,
            "newMessage": {"role": "user", "parts": [{"text": prompt}]},
        }
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None
        last = data[-1]
        parts = last.get("content", {}).get("parts", [])
        if not parts:
            return None
        return parts[0].get("text")
    except Exception:
        return local_answer(prompt)
