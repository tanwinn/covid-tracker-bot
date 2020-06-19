"""
api.main.py
"""
import logging
import os
from pathlib import Path
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from wit import Wit

# pylint: disable=logging-format-interpolation
APP_LOGGER = logging.getLogger(__name__)

# Wit.ai parameters
WIT_TOKEN = os.environ.get("WIT_TOKEN")
# Messenger API parameters
FB_PAGE_TOKEN = os.environ.get("FB_PAGE_TOKEN")
# A user secret to verify webhook get request
FB_VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN")

PRIVACY_POLICY_PATH = Path(__file__).parent.parent / "resources" / "pp.txt"


class Event(BaseModel):
    """Facebook event object"""

    object: str
    entry: List = None


app = FastAPI(
    title="Covid Tracking Bot",
    description="A Chatbot that tracks covid cases (testdrive)",
    docs_url="/",
    redoc_url="/docs",
)
wit_client = Wit(WIT_TOKEN)


@app.get("/webhook")
def messenger_webhook(request: Request):
    """
    A webhook to return a challenge
    """
    verify_token = request.query_params.get("hub.verify_token")
    # check whether the verify tokens match

    if (
        verify_token == FB_VERIFY_TOKEN
        and request.query_params.get("hub.mode") == "subscribe"
    ):
        # respond with the challenge to confirm
        try:
            resp = int(request.query_params.get("hub.challenge", "errored"))
        except ValueError:
            resp = request.query_params.get("hub.challenge", "errored")
        APP_LOGGER.debug(f"Return challenge: {type(resp)} {resp}")
        return JSONResponse(content=resp, headers={"Content-Type": "text/html"})
    APP_LOGGER.error(
        f"Invalid Request or Verification Token: given {verify_token}, expected {FB_VERIFY_TOKEN}"
    )
    return "Invalid Request or Verification Token"


@app.post("/webhook")
def messenger_post(data: Event):  # pylint: disable=unused-argument
    """
    Handler for webhook (currently for postback and messages)
    """
    return "dummy"


@app.get("/privacy-policy", response_class=HTMLResponse)
def get_privacy_policy():
    with open(PRIVACY_POLICY_PATH) as rfile:
        return rfile.read()
    return None
