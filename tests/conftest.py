"""
tests.conftest.py
~~~~~~~~~~~~~~~~~
"""

import json
import os
from pathlib import Path

import pytest
import requests
import responses
from fastapi.testclient import TestClient

from api import main, utils

ROOT = Path(__file__).joinpath("..").joinpath("..").resolve()
TEST_DATA_PATH = ROOT / "tests" / "data"
FACEBOOK_TEST_DATA_PATH = TEST_DATA_PATH / "facebook"
WIT_TEST_DATA_PATH = TEST_DATA_PATH / "wit"
TRACKER_TEST_DATA_PATH = TEST_DATA_PATH / "tracker"


@pytest.fixture(scope="session")
def test_data_path():
    return TEST_DATA_PATH


@pytest.fixture(scope="session")
def api_client():
    """FastAPI testing client"""
    return TestClient(main.APP)


@pytest.fixture
def patch_wit_client(monkeypatch, mocker):
    """Mocked wit client"""
    monkeypatch.setattr(utils, "WIT_CLIENT", value=mocker.MagicMock(specs=["message"]))
    yield
    monkeypatch.undo()


# Facebook Test data

with open(str(FACEBOOK_TEST_DATA_PATH / "messaging_data.json")) as outfile:
    MESSAGING_DATA = json.load(outfile)
    INVALID_MESSAGING_DATA = MESSAGING_DATA.get("invalid")
    VALID_MESSAGING_DATA = MESSAGING_DATA.get("valid")


@pytest.fixture(scope="session", params=VALID_MESSAGING_DATA)
def test_data_valid_messaging(request):
    """Test data for valid messaging models"""
    return request.param


@pytest.fixture(scope="session", params=INVALID_MESSAGING_DATA)
def test_data_invalid_messaging(request):
    """Test data for invalid messaging models"""
    return request.param


with open(str(FACEBOOK_TEST_DATA_PATH / "message_data.json")) as outfile:
    MESSAGE_DATA = json.load(outfile)
    INVALID_MESSAGE_DATA = MESSAGE_DATA.get("invalid")
    VALID_MESSAGE_DATA = MESSAGE_DATA.get("valid")


@pytest.fixture(scope="session", params=VALID_MESSAGE_DATA)
def test_data_valid_message(request):
    """Test data for valid message models"""
    return request.param


@pytest.fixture(scope="session", params=INVALID_MESSAGE_DATA)
def test_data_invalid_message(request):
    """Test data for invalid message models"""
    return request.param


with open(str(FACEBOOK_TEST_DATA_PATH / "event_data.json")) as outfile:
    EVENT_DATA = json.load(outfile)
    INVALID_EVENT_DATA = EVENT_DATA.get("invalid")
    VALID_EVENT_DATA = EVENT_DATA.get("valid")


@pytest.fixture(scope="session", params=VALID_EVENT_DATA)
def test_data_valid_event(request):
    """Test data for valid event models"""
    return request.param


@pytest.fixture(scope="session", params=INVALID_EVENT_DATA)
def test_data_invalid_event(request):
    """Test data for invalid event models"""
    return request.param


with open(str(FACEBOOK_TEST_DATA_PATH / "response_message_data.json")) as outfile:
    RESPONSE_MESSAGE_DATA = json.load(outfile)
    INVALID_RESPONSE_MESSAGE_DATA = RESPONSE_MESSAGE_DATA.get("invalid")
    VALID_RESPONSE_MESSAGE_DATA = RESPONSE_MESSAGE_DATA.get("valid")


@pytest.fixture(scope="session", params=VALID_RESPONSE_MESSAGE_DATA)
def test_data_valid_response_message(request):
    """Test data for valid ResponseMessage models"""
    return request.param


@pytest.fixture(scope="session", params=INVALID_RESPONSE_MESSAGE_DATA)
def test_data_invalid_response_message(request):
    """Test data for invalid ResponseMessage models"""
    return request.param


# Wit Test Data
with open(str(WIT_TEST_DATA_PATH / "text_meaning_data.json")) as outfile:
    TEXT_MEANING_DATA = json.load(outfile)
    INVALID_TEXT_MEANING_DATA = TEXT_MEANING_DATA.get("invalid")
    VALID_TEXT_MEANING_DATA = TEXT_MEANING_DATA.get("valid")


@pytest.fixture(scope="session", params=VALID_TEXT_MEANING_DATA)
def test_data_valid_text_meaning(request):
    """Test data for valid TextMeaning models"""
    return request.param


with open(str(TRACKER_TEST_DATA_PATH / "valid.json")) as outfile:
    VALID_TEST_DATA = json.load(outfile)


@pytest.fixture(scope="session")
def test_data_valid_api_location():
    """Test data for valid Location models"""
    return VALID_TEST_DATA.get("location_data")


@pytest.fixture(scope="session")
def test_data_valid_api_latest():
    """Test data for valid Latest models"""
    return VALID_TEST_DATA.get("latest_data")


@pytest.fixture(scope="session")
def test_data_valid_api_location_with_timelines():
    """Test data for valid Location w timelines models"""
    with open(
        str(TRACKER_TEST_DATA_PATH / "valid_location_w_timeline.json")
    ) as outfile:
        return json.load(outfile)


@pytest.fixture(scope="session")
def test_data_valid_api_locations_timeline():
    """Test data for valid Location w timelines models"""
    with open(str(TRACKER_TEST_DATA_PATH / "valid_locations_report.json")) as outfile:
        return json.load(outfile)


@pytest.fixture(scope="session")
def test_data_valid_api_locations(test_data_valid_api_locations_timeline):
    """Test data for valid Location without timelines models"""
    data = test_data_valid_api_locations_timeline
    data["timelines"] = {}
    return data
