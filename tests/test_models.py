"""
tests.test_models.py
~~~~~~~~~~~~~~~~~
Test models
"""

from pprint import pformat as pf

import pytest
from pydantic.error_wrappers import ValidationError

from api import models


def test_valid_user():
    kwargs = {"id": "18722912"}
    assert kwargs == models.User(**kwargs).dict(exclude_unset=True)


@pytest.mark.parametrize("id", ([], None))
def test_invalid_user(id):
    with pytest.raises(ValidationError):
        models.User(id=id).dict(exclude_unset=True)


def test_valid_messaging(test_data_valid_messaging):
    models.Messaging(**test_data_valid_messaging)


def test_invalid_messaging(test_data_invalid_messaging):
    with pytest.raises(ValidationError):
        models.Messaging(**test_data_invalid_messaging)


def test_valid_message(test_data_valid_message):
    print(f"Test Data:\n{pf(test_data_valid_message)}")
    models.Message(**test_data_valid_message)


def test_invalid_message(test_data_invalid_message):
    print(f"Test Data:\n{pf(test_data_invalid_message)}")
    with pytest.raises(ValidationError):
        models.Message(**test_data_invalid_message)


def test_valid_event(test_data_valid_event):
    print(f"Test Data:\n{pf(test_data_valid_event)}")
    models.Event(**test_data_valid_event)


def test_invalid_event(test_data_invalid_event):
    print(f"Test Data:\n{pf(test_data_invalid_event)}")
    with pytest.raises(ValidationError):
        models.Event(**test_data_invalid_event)
