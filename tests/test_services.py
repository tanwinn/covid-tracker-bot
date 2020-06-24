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
        "time,expected",
        [
            ("2020-05-01T00:00:00.000-07:00", True),
            ("2022-06-23T03:59:48.906559Z.", False),
        ],
    )
    @pytest.mark.integration
    def test_timed_by_country(self, time, expected):
        country_id = 44
        result = tracker.get_by_country(country_id, time=time)
        if expected:
            assert result.confirmed > 0
        else:
            assert result is None
        print(pf(f"Response:\n{result}"))

    @pytest.mark.parametrize(
        "time,expected",
        [
            ("2020-05-01T00:00:00.000-07:00", True),
            ("2022-06-23T03:59:48.906559Z.", False),
        ],
    )
    @pytest.mark.integration
    def test_timed_by_country_code(self, time, expected):
        country_code = "JP"
        result, valid_time = tracker.get_by_country_code(country_code, time=time)
        assert result.confirmed > 0
        assert valid_time is expected
        print(pf(f"Response:\n{result}"))


@responses.activate
def test_world_latest(test_data_valid_api_latest):
    url = f"{tracker.TRACKER_API}/latest"
    responses.add(responses.GET, url, status=200, json=test_data_valid_api_latest)
    tracker.get_world_latest()
    assert responses.assert_call_count(url, 1)


@pytest.mark.parametrize("country_id", [250, 12, 23])
@responses.activate
def test_latest_by_country(country_id, mocker, test_data_valid_api_location):
    url = f"{tracker.TRACKER_API}/locations/{country_id}?timelines=False"
    responses.add(responses.GET, url, status=200, json=test_data_valid_api_location)
    result = tracker.get_by_country(country_id)
    print(pf(f"Response:\n{result}"))
    assert responses.assert_call_count(url, 1)


@pytest.mark.parametrize(
    "time,confirmed_expected",
    [("2020-05-01T00:00:00.000-07:00", 12), ("2021-06-23T03:59:48.906559Z", None)],
)
@responses.activate
def test_timed_by_country(
    time, mocker, test_data_valid_api_location_with_timelines, confirmed_expected
):
    country_id = 44
    url = f"{tracker.TRACKER_API}/locations/{country_id}?timelines=True"
    responses.add(
        responses.GET, url, status=200, json=test_data_valid_api_location_with_timelines
    )
    result = tracker.get_by_country(country_id, time=time)
    if confirmed_expected:
        assert result.confirmed == confirmed_expected
    else:
        assert result is None
    print(pf(f"Response:\n{result}"))
    assert responses.assert_call_count(url, 1)


@pytest.mark.parametrize(
    "time,deaths_expected,valid_time",
    [
        ("2020-05-01T00:00:00.000-07:00", 65243, True),
        ("2021-06-29T00:00:00.000-07:00", 119977, False),
    ],
)
@responses.activate
def test_timed_by_country_code(
    deaths_expected, time, valid_time, test_data_valid_api_locations_timeline
):
    country_code = "US"
    url = f"{tracker.TRACKER_API}/locations?country_code={country_code}&timelines=True"
    responses.add(
        responses.GET, url, status=200, json=test_data_valid_api_locations_timeline
    )
    result, succeed = tracker.get_by_country_code(country_code, time=time)
    print(pf(f"Response:\n{result}"))
    # get the latest report and return false when invalid datetime happens
    assert result.deaths == deaths_expected
    assert valid_time == succeed
    assert responses.assert_call_count(url, 1)


@responses.activate
def test_latest_by_country_code(test_data_valid_api_locations):
    country_code = "VN"
    confirmed_expected = 2281290
    url = f"{tracker.TRACKER_API}/locations?country_code={country_code}&timelines=False"
    responses.add(responses.GET, url, status=200, json=test_data_valid_api_locations)
    result, valid_time = tracker.get_by_country_code(country_code)
    print(pf(f"Response:\n{result}"))
    assert result.confirmed == confirmed_expected
    assert valid_time
    assert responses.assert_call_count(url, 1)
