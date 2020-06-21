"""
tests.test_api.py
~~~~~~~~~~~~~~~~~
Test util methods
"""
import json
from pprint import pformat as pf

import pytest

from api import main, utils


@pytest.mark.parametrize(
    "user_id,text,token", [("tanwinn", "philodendron is the best", "cactus")]
)
def test_fb_message(mocker, monkeypatch, mocked_200_response, user_id, text, token):
    monkeypatch.setattr(utils, "FB_PAGE_TOKEN", value=token)
    post_call_mock = mocker.patch("requests.post", return_value=mocked_200_response)

    utils.fb_message(user_id, text)

    url = f"{utils.FB_GRAPH_API}access_token={token}"
    data = {"recipient": {"id": user_id}, "message": {"text": text}}

    post_call_mock.assert_called_once()
    args, kwargs = post_call_mock.call_args_list[0]
    kwargs = json.loads(kwargs.get("json"))

    assert url in args
    assert all([kwargs.get(k) == v for k, v in data.items()])

    monkeypatch.undo()
