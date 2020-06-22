"""
api.main.py
"""
import logging
import os
from pathlib import Path
from pprint import pformat as pf

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from api import utils
from models import facebook

# pylint: disable=logging-format-interpolation
APP_LOGGER = logging.getLogger(__name__)

# Messenger API parameters
FB_PAGE_TOKEN = os.environ.get("FB_PAGE_TOKEN", "default")
# A user secret to verify webhook get request
FB_VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN", "default")

ROOT = Path(__file__).joinpath("..").joinpath("..").resolve()
PRIVACY_POLICY_PATH = ROOT / "resources" / "pp.html"


APP = FastAPI(
    title="Covid Tracking Bot",
    description="A Chatbot that tracks covid cases (testdrive)",
    docs_url="/",
    redoc_url="/docs",
    version="0.0.32",
)


@APP.get("/webhook")
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
        APP_LOGGER.warning(f"Return challenge: {type(resp)} {resp}")
        return JSONResponse(content=resp, headers={"Content-Type": "text/html"})
    APP_LOGGER.error(
        f"Invalid Request or Verification Token: given {verify_token}, expected {FB_VERIFY_TOKEN}"
    )
    return "Invalid Request or Verification Token"


@APP.post("/webhook")
def messenger_post(data: facebook.Event):
    """
    Handler for webhook (currently for postback and messages)
    """
    APP_LOGGER.warning(f"Data event:\n {data}")
    for entry in data.entry:
        # get all the messages
        messages = entry.messaging
        if messages[0]:
            # Get the first message
            message = messages[0]
            APP_LOGGER.warning(f"Message object: \n{pf(message.message.dict())}")
            # Yay! We got a new message!
            texts = utils.handle_user_message(message)
            # We retrieve the Facebook user ID of the sender
            fb_id = message.sender.id
            # send message
            for text in texts:
                fb_post_resp = utils.fb_message(fb_id, text)
                APP_LOGGER.warning(
                    f"FB response after POSTing content=`{text}:\n{pf(fb_post_resp)}"
                )
    return "dummy"


@APP.get("/privacy-policy", response_class=HTMLResponse)
def get_privacy_policy():
    with open(PRIVACY_POLICY_PATH) as rfile:
        return rfile.read()
    return None
