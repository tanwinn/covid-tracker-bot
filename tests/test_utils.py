"""
tests.test_api.py
~~~~~~~~~~~~~~~~~
Test util methods
"""
import json
from pprint import pformat as pf

import pytest
import responses

from api import main, utils


@responses.activate
@pytest.mark.parametrize(
    "user_id,text,token", [("tanwinn", "philodendron is the best", "cactus")]
)
def test_fb_message(mocker, monkeypatch, user_id, text, token):
    monkeypatch.setattr(utils, "FB_PAGE_TOKEN", value=token)
    url = f"{utils.FB_GRAPH_API}access_token={token}"
    responses.add(responses.POST, url, status=200, json="mocked")
    utils.fb_message(user_id, text)
    assert responses.assert_call_count(url, 1)
    monkeypatch.undo()
