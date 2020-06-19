"""
api.main.py
"""
import logging
import os
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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

    APP_LOGGER.info("testing info log")
    print(f"verify_token: {verify_token}, envvar: {FB_VERIFY_TOKEN}")
    APP_LOGGER.warning(f"LOG:: verify_token: {verify_token}, envvar: {FB_VERIFY_TOKEN}")

    if (
        verify_token == FB_VERIFY_TOKEN
        and request.query_params.get("hub.mode") == "subscribe"
    ):
        # respond with the challenge to confirm
        resp = request.query_params.get("hub.challenge", "errored")
        APP_LOGGER.warning(f"Return challenge: {resp}")
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
    # if data.object == "page":
    #     # boilerplate code
    #     for entry in data.entry:
    #         messages = entry["messaging"]
    #         if messages[0]:
    #             # Get the first message
    #             message = messages[0]
    #             # Yay! We got a new message!
    #             # We retrieve the Facebook user ID of the sender
    #             fb_id = message["sender"]["id"]
    #             # We retrieve the message content
    #             text = message["message"]["text"]
    #             # Let's forward the message to Wit /message
    #             # and customize our response to the message in handle_message
    #             response = client.message(msg=text, context={"session_id": fb_id})
    #             handle_message(response=response, fb_id=fb_id)
    return "dummy"
