# pylint: disable=logging-format-interpolation
import json
import logging
from pathlib import Path

ROOT = Path(__file__).joinpath("..").joinpath("..").resolve()

LOGGER = logging.getLogger(__name__)


LOGGER.warning("LOADING COUNTRY CODE DATA...")
with open(str(ROOT / "data" / "country_codes_temp.json")) as outfile:
    CODES = json.load(outfile)


def country_code(name: str) -> str:
    """Get two letter country code based on name"""
    LOGGER.warning(f"Getting country_code for {name}...")
    return CODES.get(name)
