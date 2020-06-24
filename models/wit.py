"""
models.wit.py
~~~~~~~~~~~~~~~~~~~~~~
Wit models
"""
import enum
from typing import Dict, List

from pydantic import BaseModel, Field, root_validator


class Coordinations(BaseModel):
    """Coordinates model"""

    lat: float
    long: float


class Location(BaseModel):
    """resolved/computed location model"""

    name: str
    domain: str = None
    coords: Coordinations = None
    timezone: str = None
    external: Dict = None


class LocationList(BaseModel):
    values: List[Location]


class WitLocationType(enum.Enum):
    """either value or resolved"""

    UNRESOLVED = "value"
    RESOLVED = "resolved"


class WitLocation(BaseModel):
    """wit/location model"""

    confidence: float
    value: str = None
    resolved: LocationList = None
    body: str = Field(..., description="Literal content from the original text")
    type: WitLocationType

    @root_validator
    @classmethod
    def root_validator(cls, values):
        if (
            values.get("type") == WitLocationType.RESOLVED.value
            and values.get("resolved") is None
        ):
            raise ValueError("Resolved WitLocation type must have `resolved` attribute")
        if (
            values.get("type") == WitLocationType.UNRESOLVED.value
            and values.get("value") is None
        ):
            raise ValueError("Value WitLocation type must have `value` attribute")
        return values


class Datetime(BaseModel):
    """computed/resolved datetime model powered by duckling"""

    value: str = None  # TODO: parse this into datetime type
    grain: str = None


class WitDatetimeType(enum.Enum):
    """WitDatetimeType enum value"""

    VALUE = "value"
    INTERVAL = "interval"


class WitDatetime(BaseModel):
    """wit/datetime model"""

    body: str = Field(..., description="Literal content from the original text")
    confidence: float
    values: List[Datetime] = None
    value: str = None  # TODO: parse this into datetime type
    type: WitDatetimeType


class IntentName(enum.Enum):
    """Intent name registered"""

    BEGIN = "getting_started"
    QUERY = "get_by_country"


class Intent(BaseModel):
    """Wit intent model"""

    id: str
    name: IntentName
    confidence: float


class Entities(BaseModel):
    """Entity type registered"""

    location: List[WitLocation] = Field(None, alias="wit$location:location")
    datetime: List[WitDatetime] = Field(None, alias="wit$datetime:datetime")


class WitGreeting(BaseModel):
    """Greeting model"""

    value: bool
    confidence: float


class Traits(BaseModel):
    """Traits model"""

    greetings: List[WitGreeting] = Field(None, alias="wit$greetings")


class TextMeaning(BaseModel):
    """GET /message response from Wit"""

    text: str
    entities: Entities
    intents: List[Intent]
    traits: Traits = {}


class ScriptInput(BaseModel):
    countries: List[str] = Field(None, example=["Vietnam", "Laos"])
