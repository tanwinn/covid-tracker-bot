"""
models.facebook.py
~~~~~~~~~~~~~~~~~~~~~~
Facebook Message models
"""
from typing import Dict, List

from pydantic import BaseModel, Field, root_validator, validator


class User(BaseModel):
    """User model"""

    id: str


class Message(BaseModel):
    """Message model"""

    mid: str
    text: str = None
    quick_reply: Dict = None
    reply_to: Dict = None
    attachments: Dict = None

    @root_validator
    @classmethod
    def must_have_content(cls, values):
        if all([values.get(k) is None for k in ["text", "quick_reply", "attachments"]]):
            raise ValueError("Message object must have content")
        return values


class Messaging(BaseModel):
    """Messaging object"""

    sender: User
    recipient: User
    timestamp: int
    message: Message


class MessageEvent(BaseModel):
    """MessageEvent models in webhook event"""

    id: str
    time: int
    messaging: List[Messaging]


class Event(BaseModel):
    """Webhook event model"""

    object: str = Field(example="page")
    entry: List[MessageEvent] = None

    @validator("object")
    @classmethod
    def object_must_be_page(cls, value):
        if value == "page":
            return value
        raise ValueError("object must be page")


class ResponseMessage(BaseModel):
    """ResponseMessage of Response model"""

    text: str


class Response(BaseModel):
    """Chatbot's Response model back to the Facebook sending user"""

    message: ResponseMessage
    recipient: User
