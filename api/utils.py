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
GETTING_STARTED_SCRIPT = (
    "Hi there, welcome to COVID-19 Tracker Chatbot! "
    "We are here to provide you on number of COVID-19 infected, and death cases in countries worldwide. "
    "Recovered case information is not supported by our current source - John Hopkins University (JHU)."
)
INSTRUCTIONS_SCRIPT = "Please enter the country and corresponding time period you want to learn about (ie. United States last month)."

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
    locations_arg = []
    resolved_countries = []
    if locations:
        LOGGER.warning("We have location entities")
        for location in locations:
            LOGGER.debug(f"processing location: {location.body}: type: {location.type}")
            LOGGER.debug(f"current arg: {pf(locations_arg)}")
            if location.type == wit.WitLocationType.UNRESOLVED:
                locations_arg.append(f"unresolved location {location.value}")
                resolved_countries.append(location.value)
            else:
                resolved_values = location.resolved.values
                resolved_country = None
                LOGGER.debug(f"resolving values")
                for v in resolved_values:
                    LOGGER.warning(f"\t{v.name}: {v.domain}")
                    if v.domain == "country":
                        locations_arg.append(f"resolved country {v.name}")
                        resolved_country = v.name
                        break
                resolved_countries.append(
                    resolved_country if resolved_country else resolved_values[0].name
                )
    return ", ".join(locations_arg), resolved_countries


def handle_time(meaning: wit.TextMeaning) -> str:
    """"Extract time info from wit"""
    # one day specifically
    times = meaning.entities.datetime
    time_arg = None
    if times:
        time_arg = times[0]
        LOGGER.warning(f"len(times): {len(times)}")
        if len(times) > 1 or time_arg.type == wit.WitDatetimeType.INTERVAL:
            return "invalid"
        time_arg = time_arg.value
    return time_arg


def handle_query(countries: List[str], time: str = None):
    text = []
    source = "JHU"
    LOGGER.warning(f"Countries = {countries}")
    if not countries:
        text.append(
            f"I couldn't detect the coutry you provide. Please make sure the spelling is correct."
        )
    for country_name in countries:
        country_code = data.country_code(country_name)
        LOGGER.warning(f"Getting info for {country_name}: {country_code}")
        if not country_code:
            text.append(
                f"{source} doesn't support {country_name} :( Please enter a valid country name and/or time period. Thank you! "
            )
            continue
        try:
            result, valid_time = tracker.get_by_country_code(country_code, time)
            LOGGER.warning(f"Result: {result}")
            if not valid_time:
                text.append(
                    f"{source} doesn't have info for {country_name} in {time[:10]}. I'll give you the latest info."
                )
                time = None
            text.append(
                f"By {time[:10] if time else tracker.last_updated()}, "
                f"{country_name} has {format(result.confirmed, ',d')} confirmed cases"
                f" and {format(result.deaths, ',d')} death cases."
            )
        except (requests.HTTPError):
            text.append(
                f"{source} doesn't support {country_name} with country code {country_code} :("
            )
        except requests.ConnectionError:
            # TODO: add handover protocol
            text.append(f"API is currently down. Can't get the info.")
    return text


def handle_oos_intent(meaning: wit.TextMeaning):  # pylint: disable=unused-argument
    reply = ["I don't understand ", INSTRUCTIONS_SCRIPT]
    return reply


def handle_query_intent(meaning: wit.TextMeaning) -> List[str]:
    reply = []
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
        reply.append(f"Location(s):{locations_arg}")

    LOGGER.warning(
        f"Handling query for countries {resolved_countries} & time {time_arg}..."
    )
    reply.extend(handle_query(resolved_countries, time_arg))
    return reply


# pylint: disable=too-many-nested-blocks
def handle_user_message(fb_message_object) -> List[str]:
    """Interpret user_msg's intent & entities using Wit"""

    try:
        text = fb_message_object.message.text
        reply = [f"We've received your message: {text}"]
        response = WIT_CLIENT.message(msg=text)
        LOGGER.debug(f"WIT response:\n{pf(response)}")
        meaning = wit.TextMeaning.parse_obj(response)
        intent = meaning.intents[0].name if meaning.intents else "oos"
        reply.append(f"Intents: {intent}")
        if intent == "oos":
            reply.extend(handle_oos_intent(meaning))
        else:
            reply.extend(handle_query_intent(meaning))
    except Exception as err:
        LOGGER.error(f"Dismissed ERROR:\n{pf(err)}")
    return "\n".join(reply)
