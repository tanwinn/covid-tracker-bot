"""
tests.test_facebook.py
~~~~~~~~~~~~~~~~~
Test models
"""

from pprint import pformat as pf

import pytest
from pydantic.error_wrappers import ValidationError

from models import facebook, wit


class TestFacebook:
    """Test Facebook models"""

    def test_valid_user(self):
        kwargs = {"id": "18722912"}
        assert kwargs == facebook.User(**kwargs).dict(exclude_unset=True)

    @pytest.mark.parametrize("id", ([], None))
    def test_invalid_user(self, id):
        with pytest.raises(ValidationError):
            facebook.User(id=id).dict(exclude_unset=True)

    def test_valid_messaging(self, test_data_valid_messaging):
        facebook.Messaging(**test_data_valid_messaging)

    def test_invalid_messaging(self, test_data_invalid_messaging):
        with pytest.raises(ValidationError):
            facebook.Messaging(**test_data_invalid_messaging)

    def test_valid_message(self, test_data_valid_message):
        print(f"Test Data:\n{pf(test_data_valid_message)}")
        facebook.Message(**test_data_valid_message)

    def test_invalid_message(self, test_data_invalid_message):
        print(f"Test Data:\n{pf(test_data_invalid_message)}")
        with pytest.raises(ValidationError):
            facebook.Message(**test_data_invalid_message)

    def test_valid_event(self, test_data_valid_event):
        print(f"Test Data:\n{pf(test_data_valid_event)}")
        facebook.Event(**test_data_valid_event)

    def test_invalid_event(self, test_data_invalid_event):
        print(f"Test Data:\n{pf(test_data_invalid_event)}")
        with pytest.raises(ValidationError):
            facebook.Event(**test_data_invalid_event)

    def test_valid_response_message(self, test_data_valid_response_message):
        print(f"Test Data:\n{pf(test_data_valid_response_message)}")
        facebook.Response(**test_data_valid_response_message)

    def test_invalid_response_message(self, test_data_invalid_response_message):
        print(f"Test Data:\n{pf(test_data_invalid_response_message)}")
        with pytest.raises(ValidationError):
            facebook.Response(**test_data_invalid_response_message)


class TestWit:
    """Test Wit models"""

    def test_valid_text_meaning(self, test_data_valid_text_meaning):
        print(f"Test Data:\n{pf(test_data_valid_text_meaning)}")
        wit.TextMeaning(**test_data_valid_text_meaning)
