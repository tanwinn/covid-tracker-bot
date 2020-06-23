"""
api.utils.py
~~~~~~~~~~~~
Utilities used by api.
"""
# pylint: disable=logging-format-interpolation
# TODO: better name

import logging
import os
from pprint import pformat as pf
from typing import List

import requests
from wit import Wit

import data
from api import tracker
from models import facebook, wit

WIT_TOKEN = os.environ.get("WIT_TOKEN", "default")
FB_PAGE_TOKEN = os.environ.get("FB_PAGE_TOKEN", "default")
FB_GRAPH_API = "https://graph.facebook.com/me/messages?"

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


def handle_location(meaning: wit.TextMeaning) -> (str, List[str]):
    """Extract locations info from wit"""
    locations = meaning.entities.location
    locations_arg = ""
    resolved_countries = []
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
                        resolved_countries.append(v.name)
                        break
    return locations_arg, resolved_countries


def handle_time(meaning: wit.TextMeaning) -> str:
    """"Extract time info from wit"""
    # one day specifically
    times = meaning.entities.datetime
    time_arg = None
    if times:
        time_arg = times[0]
        print(f"len(times): {len(times)}")
        if len(times) > 1 or time_arg.type == wit.WitDatetimeType.INTERVAL:
            return "invalid"
        time_arg = time_arg.value
    return time_arg


def handle_query(countries: List[str], time: str = None):
    text = []
    LOGGER.warning(f"Countries={countries}")
    for country_name in countries:
        country_code = data.country_code(country_name)
        LOGGER.warning(f"Getting info for {country_name}: {country_code}")
        if country_code:
            result = tracker.get_by_country_code(country_code, time)
            LOGGER.warning(f"Result: {result}")
            text.append(f"COVID situation in {country_name}: {result}")
    return "\n".join(text)


# pylint: disable=too-many-nested-blocks
def handle_user_message(fb_message_object) -> List[str]:
    """Interpret user_msg's intent & entities using Wit"""

    text = fb_message_object.message.text
    reply = [f"We've received your message: {text}"]
    try:
        response = WIT_CLIENT.message(msg=text)
        LOGGER.warning(f"WIT response:\n{pf(response)}")
        meaning = wit.TextMeaning.parse_obj(response)
        reply.append(
            f"Intents: {meaning.intents[0].name if meaning.intents else 'out of scope'}"
        )
        time_arg = handle_time(meaning)
        locations_arg, resolved_countries = handle_location(meaning)
        if time_arg == "invalid":
            reply.append(
                f"I can only provide COVID cases on a certain date. I'll give you the latest info."
            )
            time_arg = None
        elif time_arg:
            reply.append(f"Time: {time_arg}")

        if locations_arg != "":
            reply.append(f"Location(s):{locations_arg[:-1]}")

        LOGGER.warning(
            f"Handling query for countries {resolved_countries} & time {time_arg}..."
        )
        query_result = handle_query(resolved_countries, time_arg)
        if query_result != "":
            reply.append(query_result)

    except Exception:
        pass
    return reply
