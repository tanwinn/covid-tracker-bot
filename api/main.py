"""
api.main.py
"""
import logging
import os
from pathlib import Path
from pprint import pformat as pf
from typing import List

import requests
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

ROOT = Path(__file__).joinpath("..").joinpath("..").resolve()
PRIVACY_POLICY_PATH = ROOT / "resources" / "pp.txt"


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
    if data.object == "page":
        for entry in data.entry:
            # get all the messages
            messages = entry["messaging"]
            if messages[0]:
                # Get the first message
                message = messages[0]
                APP_LOGGER.warning(f"THE MESSAGE OBJECT: \n{pf(message)}")
                # Yay! We got a new message!
                # We retrieve the Facebook user ID of the sender
                fb_id = message["sender"]["id"]
                # We retrieve the message content
                text = message["message"]["text"]
                # Let's forward the message to Wit /message
                # and customize our response to the message in handle_message
                response = wit_client.message(msg=text)
                print(pf(response))
                handle_message(response=response, fb_id=fb_id)
    else:
        # Returned another event
        return "Received Different Event"
    return "dummy"


def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    data = {"recipient": {"id": sender_id}, "message": {"text": text}}
    # Setup the query string with your PAGE TOKEN
    qs = "access_token=" + FB_PAGE_TOKEN
    # Send POST request to messenger
    resp = requests.post("https://graph.facebook.com/me/messages?" + qs, json=data)
    return resp.content


def first_trait_value(traits, trait):
    """
    Returns first trait value
    """
    if trait not in traits:
        return None
    val = traits[trait][0]["value"]
    if not val:
        return None
    return val


def handle_message(response, fb_id):
    """
    Customizes our response to the message and sends it
    """
    # Checks if user's message is a greeting
    # Otherwise we will just repeat what they sent us
    greetings = first_trait_value(response["traits"], "wit$greetings")
    if greetings:
        text = "hello!"
    else:
        text = "We've received your message: " + response["_text"]
    # send message
    print(f"FB response: {pf(fb_message(fb_id, text))}")


@app.get("/privacy-policy", response_class=HTMLResponse)
def get_privacy_policy():
    with open(PRIVACY_POLICY_PATH) as rfile:
        return rfile.read()
    return None
