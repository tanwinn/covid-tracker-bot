"""
tests.test_api.py
~~~~~~~~~~~~~~~~~
Test api calls
"""

import json
from pprint import pformat as pf

import pytest

import api


def test_client(api_client):
    assert api_client


@pytest.mark.parametrize(
    "params", ["hub.verify_token=invalid", "hub.verify_token=foo&hub.challenge=bar"]
)
def test_webhook_always_return_200(api_client, params):
    assert api_client.get(f"/webhook?{params}").status_code == 200


@pytest.mark.parametrize(
    "params",
    [
        "hub.verify_token=invalid&hub.mode=subscribe",
        "hub.verify_token=foo",
        "hub.verify_token=foobar&hub.mode=unsubscribe",
    ],
)
def test_get_webhook_failed(api_client, params, monkeypatch):
    monkeypatch.setattr(api.main, "FB_VERIFY_TOKEN", value="foobar")
    response = api_client.get(f"/webhook?{params}")
    assert response.json() == "Invalid Request or Verification Token"
    monkeypatch.undo()


@pytest.mark.parametrize("token,challenge", [("foo", 123), ("flamingo", "ant")])
def test_get_webhook_succeeded(api_client, token, challenge, monkeypatch):
    monkeypatch.setattr(api.main, "FB_VERIFY_TOKEN", value=token)
    response = api_client.get(
        f"/webhook?hub.verify_token={token}&hub.challenge={challenge}&hub.mode=subscribe"
    )
    assert response.json() == challenge
    monkeypatch.undo()


def test_get_privacy_policy(api_client):
    assert api_client.get("/privacy-policy").status_code == 200


def test_post_message_200_resp_valid_data(api_client, test_data_valid_event, mocker):
    mocker.patch("api.utils.handle_user_message", return_value="mocked response")
    resp = api_client.post(f"/webhook", data=json.dumps(test_data_valid_event))
    print(f"Response: \n{pf(resp.json())}")
    assert resp.status_code == 200
