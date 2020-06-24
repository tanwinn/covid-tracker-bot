"""
api.main.py
"""
import logging
import os
from pprint import pformat as pf
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

import data
from api import utils
from models import facebook

# pylint: disable=logging-format-interpolation
LOGGER = logging.getLogger(__name__)

# A user secret to verify webhook get request
FB_VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN", "default")

PRIVACY_POLICY_PATH = data.ROOT / "resources" / "pp.html"


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
        LOGGER.warning(f"Return challenge: {type(resp)} {resp}")
        return JSONResponse(content=resp, headers={"Content-Type": "text/html"})
    LOGGER.error(
        f"Invalid Request or Verification Token: given {verify_token}, expected {FB_VERIFY_TOKEN}"
    )
    return "Invalid Request or Verification Token"


@APP.post("/webhook")
def messenger_post(data: facebook.Event) -> List[str]:
    """
    Handler for webhook (currently for postback and messages)
    """
    LOGGER.warning(f"Data event:\n {pf(data.dict())}")
    for entry in data.entry:
        messages = entry.messaging
        if messages[0]:
            message = messages[0]
            LOGGER.warning(f"Message object: \n{pf(message.message.dict())}")
            text = utils.handle_user_message(message)
            # We retrieve the Facebook user ID of the sender
            fb_id = message.sender.id
            # send message
            fb_post_resp = utils.fb_message(fb_id, text)
            LOGGER.warning(
                f"FB response after POSTing content=`{text}:\n{pf(fb_post_resp)}"
            )
    return text


@APP.get("/privacy-policy", response_class=HTMLResponse)
def get_privacy_policy():
    with open(PRIVACY_POLICY_PATH) as rfile:
        return rfile.read()
    return None


# @APP.get("/execute_scripts")
# def script(file_name: str = None):
#     if file_name:
#         return data.merge_two_columns_into_dict(file_name)
#     return data.merge_two_columns_into_dict()


# @APP.post("/get-wit")
# def get_wit_method(countries: wit.ScriptInput):
#     return get_wit.get_wit(countries.countries)


# @APP.get("/map-unwit-wit")
# def map_datasset(unwit_to_cc_name: str, unwit_to_wit_name: str):
#     return data.map_wit_unwit_to_cc(unwit_to_wit_name, unwit_to_cc_name)


# @APP.get("/merge_dataset")
# def merge_dataset(unwit: str, wit: str):
#     return data.merge_wit_unwit(unwit, wit)
