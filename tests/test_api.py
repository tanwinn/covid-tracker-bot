"""
tests.test_api.py
~~~~~~~~~~~~~~~~~
"""

import pytest

import api


def test_client(api_client):
    assert api_client


@pytest.mark.parametrize(
    "params", ["hub.verify_token=invalid", "hub.verify_token=foo&hub.challenge=bar"]
)
def test_webhook_always_return_200(api_client, params):
    assert api_client.get(f"/webhook?{params}").status_code == 200


@pytest.mark.parametrize("params", ["hub.verify_token=invalid", "hub.verify_token=foo"])
def test_get_webhook_failed(api_client, params):
    response = api_client.get(f"/webhook?{params}")
    assert response.json() == "Invalid Request or Verification Token"


@pytest.mark.parametrize("token,challenge", [("foo", "123"), ("flamingo", "ant")])
def test_get_webhook_succeeded(api_client, token, challenge, monkeypatch):
    monkeypatch.setattr(api.main, "FB_VERIFY_TOKEN", value=token)
    response = api_client.get(
        f"/webhook?hub.verify_token={token}&hub.challenge={challenge}"
    )
    assert response.json() == challenge
    monkeypatch.undo()
