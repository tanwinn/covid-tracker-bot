"""
models.tracker.py
~~~~~~~~~~~~~~~~~
Models for external covid tracker API
"""
from typing import Dict, List

from pydantic import BaseModel


class Report(BaseModel):
    """Base report mode"""

    confirmed: int
    deaths: int
    # recovered: int


class Latest(BaseModel):
    """latest report model"""

    latest: Report


class Timeline(BaseModel):
    """
    Timeline model.
    """

    latest: int
    timeline: Dict[str, int] = {}


class Timelines(BaseModel):
    """
    Timelines model.
    """

    confirmed: Timeline
    deaths: Timeline
    recovered: Timeline


class Location(BaseModel):
    """
    Location model.
    """

    id: int
    country: str
    country_code: str
    country_population: int = None
    province: str = ""
    county: str = ""
    last_updated: str  # TODO use datetime.datetime type.
    coordinates: Dict
    latest: Report
    timelines: Timelines = None


class LocationReport(BaseModel):
    latest: Report


class LocationsReport(BaseModel):
    """
    Response for locations.
    """

    latest: Report
    locations: List[Location] = []
