"""
api.tracker.py
~~~~~~~~~~~~~~~
external service call
"""
# pylint: disable=logging-format-interpolation
import json
import logging
import os
from pprint import pformat as pf

import requests
from pydantic.error_wrappers import ValidationError

from models import tracker

TRACKER_API = os.environ.get("TRACKER_API", "https://127.0.0.1:8900")

LOGGER = logging.getLogger(__name__)

GLOBAL = {}


class NotFoundError(Exception):
    """NotFound Exception"""


def _call(path, raise_err=True, **kwargs):
    url = f"{TRACKER_API}{path}"
    LOGGER.warning(f"Prepping calls to GET {url}...")
    resp = requests.get(url, params=kwargs)
    # LOGGER.warning(f"Response {resp.status_code}:")
    try:
        LOGGER.warning(f"\t{pf(resp.json())}")
    except json.decoder.JSONDecodeError:
        LOGGER.warning(f"\t{pf(resp.text)}")

    try:
        resp.raise_for_status()
    except (requests.HTTPError, requests.ConnectionError) as err:
        if raise_err:
            if resp.status_code != 404:
                raise err
            raise NotFoundError
        LOGGER.error(f"Dismissed error: \n{err}")
    return resp


def get_world_latest() -> tracker.Report:
    resp = _call("/latest")
    return tracker.Latest.parse_obj(resp.json()).latest


def get_by_country(country_id: int, time: str = None) -> tracker.Report:
    """bool: means if the time requested succeeded"""
    timelines = time is not None
    location_object = dict(
        _call(f"/locations/{country_id}", timelines=timelines).json()
    ).get("location")
    LOGGER.warning(f"Location object:\n{pf(location_object)}")
    if not timelines:
        location_object.pop("timelines", None)
        return tracker.Location.parse_obj(location_object).latest
    return get_by_time(tracker.Location.parse_obj(location_object), time)


def update_last_updated(location: tracker.Location):
    """Make sure the latest_update time is correct"""
    last_update = location.last_updated[:10]
    GLOBAL.update({"last_update": last_update})


def last_updated() -> str:
    """return the last update tim period"""
    return GLOBAL.get("last_update")


def get_by_country_code(country_code: str, time: str = None) -> (tracker.Report, bool):
    """bool: means if the time requested succeeded"""
    timelines = time is not None
    locations_object = tracker.LocationsReport.parse_obj(
        _call(f"/locations", country_code=country_code, timelines=timelines).json()
    )
    LOGGER.debug(f"Locations object:\n{pf(locations_object)}")
    result = None
    valid_time = True
    update_last_updated(locations_object.locations[0])
    if timelines:
        result = get_by_time(locations_object.locations.pop(), time)
        valid_time = result is not None or time[:10] == last_updated()
        LOGGER.warning(f"timed result: {result}")
    LOGGER.warning(f"latest result: {locations_object.latest}")
    return (result if result else locations_object.latest), valid_time


def get_by_time(location_data, time: str) -> tracker.Report:
    """Currently support one date specifically only"""
    datetime = time[:10] + "T00:00:00Z"
    LOGGER.warning(f"Getting cases on date: {datetime}")
    data = location_data.timelines
    try:
        return tracker.Report(
            confirmed=data.confirmed.timeline.get(datetime),
            deaths=data.deaths.timeline.get(datetime),
            # recovered=data.recovered.timeline.get(datetime, 0),
        )
    except ValidationError:
        return None
