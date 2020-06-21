"""
models.wit.py
~~~~~~~~~~~~~~~~~~~~~~
Wit models
"""
import enum
from typing import Dict, List

from pydantic import BaseModel, Field


class Coordinations(BaseModel):
    """Coordinates model"""

    lat: float
    long: float


class GrainType(enum.Enum):
    locality = "locality"
    region = "region"
    country = "country"


class Location(BaseModel):
    """resolved/computed location model"""

    name: str
    grain: GrainType
    coords: Coordinations = None
    timezone: str = None
    external: Dict = None


class LocationList(BaseModel):
    resolved: List[Location]


class WitLocation(BaseModel):
    """wit/location model"""

    confidence: float
    value: str
    resolved: LocationList
    body: str = Field(..., description="Literal content from the original text")


class Datetime(BaseModel):
    """computed/resolved datetime model powered by duckling"""

    value: str  # TODO: parse this into datetime type
    grain: str


class WitDatetimeType(enum.Enum):
    """WitDatetimeType enum value"""

    value = "value"
    interval = "interval"


class WitDatetime(BaseModel):
    """wit/datetime model"""

    body: str = Field(..., description="Literal content from the original text")
    confidence: float
    values: List[Datetime] = None
    value: str  # TODO: parse this into datetime type
    type: WitDatetimeType
    to: Datetime = None
    from_val: Datetime = Field(None, alias="from")


class IntentName(enum.Enum):
    """Intent name registered"""

    begin = "getting_started"
    query = "get_by_country"


class Intent(BaseModel):
    """Wit intent model"""

    id: str
    name: IntentName
    confidence: float


class Entities(enum.Enum):
    """Entity type registered"""

    location: List[WitLocation] = Field(..., alias="wit$location:location")
    datetime: List[WitDatetime] = Field(..., alias="wit$datetime:datetime")


class TextMeaning(BaseModel):
    """GET /message response from Wit"""

    text: str
    entities: Entities
    intents: List[Intent]
