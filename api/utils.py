"""
api.utils.py
~~~~~~~~~~~~
Utilities used by api.
"""
# TODO: better name

import logging
import os
from pprint import pformat as pf
from typing import List

import requests
from wit import Wit

from models import facebook, wit

WIT_TOKEN = os.environ.get("WIT_TOKEN", "default")
FB_PAGE_TOKEN = os.environ.get("FB_PAGE_TOKEN", "default")
FB_VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN", "default")
FB_GRAPH_API = "https://graph.facebook.com/me/messages?"

# pylint: disable=logging-format-interpolation
LOGGER = logging.getLogger(__name__)

WIT_CLIENT = Wit(WIT_TOKEN)


def fb_message(sender_id, text):
    """
    Compose a message/reply to `sender_id` with content of `text`
    and send it to Messenger through POST call to FB_GRAPH_API
    """
    data = facebook.Response(
        recipient=facebook.User(id=sender_id),
        message=facebook.ResponseMessage(text=text),
    ).dict()
    LOGGER.warning(f"Prepping call to facebook with data={pf(data)}")
    resp = requests.post(f"{FB_GRAPH_API}access_token={FB_PAGE_TOKEN}", json=data)
    return resp.json()


# pylint: disable=too-many-nested-blocks
def handle_user_message(fb_message_object) -> List[str]:
    """
    Interpret user_msg's intent & entities using Wit
    """
    # We retrieve the message content
    text = fb_message_object.message.text
    # Let's forward the message to Wit /message
    # and customize our response to the message in handle_message
    reply = [f"We've received your message: {text}"]
    try:
        response = WIT_CLIENT.message(msg=text)
        LOGGER.warning(f"WIT response:\n{pf(response)}")
        # if response.get("entities")
        meaning = wit.TextMeaning.parse_obj(response)
        reply.append(
            f"Intents: {meaning.intents[0].name if meaning.intents else 'out of scope'}"
        )
        # countries
        # one day specifically
        times = meaning.entities.datetime
        time_arg = None
        if times:
            time_arg = times[0]
            print(f"len(times): {len(times)}")
            if len(times) > 1 or time_arg.type == wit.WitDatetimeType.INTERVAL:
                reply.append(f"I can only provide COVID cases on a certain date")
                time_arg = None
            time_arg = time_arg.value

        locations = meaning.entities.location
        locations_arg = ""
        if locations:
            print("We have location entities")
            for location in locations:
                (print(f"processing location: {location.body}: type: {location.type}"))
                print(f"current arg: {pf(locations_arg)}")
                if location.type == wit.WitLocationType.UNRESOLVED:
                    locations_arg += f" unresolved location {location.value},"
                else:
                    resolved_values = location.resolved.values
                    print(f"resolving values")
                    for v in resolved_values:
                        print(f"\t{v.name}: {v.domain}")
                        if v.domain == "country":
                            locations_arg += f" resolved country {v.name},"
                            break
        if time_arg:
            reply.append(f"Time: {time_arg}")

        if locations_arg != "":
            reply.append(f"Location(s):{locations_arg[:-1]}")

    except Exception:
        pass
    return reply
