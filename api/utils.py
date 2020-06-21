"""
api.utils.py
~~~~~~~~~~~~
Utilities used by api.
"""
# TODO: better name

import logging
import os
from pprint import pformat as pf

import requests
from wit import Wit

from models import facebook

WIT_TOKEN = os.environ.get("WIT_TOKEN")
FB_PAGE_TOKEN = os.environ.get("FB_PAGE_TOKEN")
FB_VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN")
FB_GRAPH_API = "https://graph.facebook.com/me/messages?"

# pylint: disable=logging-format-interpolation
UTILS_LOGGER = logging.getLogger(__name__)

wit_client = Wit(WIT_TOKEN)


def fb_message(sender_id, text):
    """
    Compose a message/reply to `sender_id` with content of `text`
    and send it to Messenger through POST call to FB_GRAPH_API
    """
    data = facebook.Response(
        recipient=facebook.User(id=sender_id),
        message=facebook.ResponseMessage(text=text),
    ).json()
    resp = requests.post(f"{FB_GRAPH_API}access_token={FB_PAGE_TOKEN}", json=data)
    return resp.json()


def handle_user_message(fb_message_object):
    """
    Interpret user_msg's intent & entities using Wit
    """
    # We retrieve the message content
    text = fb_message_object.message.text
    # Let's forward the message to Wit /message
    # and customize our response to the message in handle_message
    response = wit_client.message(msg=text)
    UTILS_LOGGER.warning(f"WIT response:\n{pf(response)}")
    # Checks if user's message is a greeting
    # Otherwise we will just repeat what they sent us
    return "We've received your message: " + response["text"]
