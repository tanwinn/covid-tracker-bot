import json
import os
from pprint import pformat as pf

import pytest
import responses

from api import tracker


class TestIntegration:
    """Integration tests"""

    @pytest.mark.integration
    def test_world_latest(self):
        tracker.get_world_latest()

    @pytest.mark.integration
    def test_latest_by_country(self):
        result = tracker.get_by_country(225)
        print(pf(f"Response:\n{result}"))

    @pytest.mark.parametrize(
        "time", ["2020-05-01T00:00:00.000-07:00", "2020-06-15T00:00:00.000-07:00"]
    )
    @pytest.mark.integration
    def test_timed_by_country(self, time):
        country_id = 44
        result = tracker.get_by_country(country_id, time=time)
        print(pf(f"Response:\n{result}"))


@responses.activate
def test_world_latest(test_data_valid_api_latest):
    url = f"{tracker.TRACKER_API}/latest"
    responses.add(responses.GET, url, status=200, json=test_data_valid_api_latest)
    tracker.get_world_latest()
    assert responses.assert_call_count(url, 1)


@pytest.mark.parametrize("country_id", [250, 12, 23])
@responses.activate
def test_latest_by_country(
    monkeypatch, country_id, mocker, test_data_valid_api_location
):
    url = f"{tracker.TRACKER_API}/locations/{country_id}?timelines=False"
    responses.add(responses.GET, url, status=200, json=test_data_valid_api_location)
    result = tracker.get_by_country(country_id)
    print(pf(f"Response:\n{result}"))
    assert responses.assert_call_count(url, 1)


@pytest.mark.parametrize(
    "time", ["2020-05-01T00:00:00.000-07:00", "2020-06-15T00:00:00.000-07:00"]
)
@responses.activate
def test_timed_by_country(
    monkeypatch, time, mocker, test_data_valid_api_location_with_timelines
):
    country_id = 44
    url = f"{tracker.TRACKER_API}/locations/{country_id}?timelines=True"
    responses.add(
        responses.GET, url, status=200, json=test_data_valid_api_location_with_timelines
    )
    result = tracker.get_by_country(country_id, time=time)
    print(pf(f"Response:\n{result}"))
    assert responses.assert_call_count(url, 1)
