"""
api.main.py
"""
import logging
import os

import uvicorn
from fastapi import FastAPI, Request
from wit import Wit

# pylint: disable=logging-format-interpolation
APP_LOGGER = logging.getLogger(__name__)

CONFIG = os.environ
# Wit.ai parameters
WIT_TOKEN = os.environ.get("WIT_TOKEN")
# Messenger API parameters
FB_PAGE_TOKEN = os.environ.get("FB_PAGE_TOKEN")
# A user secret to verify webhook get request
FB_VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN")


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
    if verify_token == FB_VERIFY_TOKEN:
        # respond with the challenge to confirm
        return request.query_params.get("hub.challenge", "errored")
    APP_LOGGER.error("Invalid Request or Verification Token")
    return "Invalid Request or Verification Token"


@app.post("/webhook")
def messenger_post():
    """
    Handler for webhook (currently for postback and messages)
    """


if __name__ == "__main__":
    uvicorn.run(
        "api.main:app", host="127.0.0.1", log_level="debug",
    )
