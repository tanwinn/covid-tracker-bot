import json
import logging
from pathlib import Path
from typing import Dict
# pylint: disable=logging-format-interpolation

ROOT = Path(__file__).joinpath("..").joinpath("..").resolve()

LOGGER = logging.getLogger(__name__)


def _load_code_data() -> Dict:
    LOGGER.warning("LOADING COUNTRY CODE DATA...")
    with open(str(ROOT / "data" / "country_codes_temp.json")) as outfile:
        return json.load(outfile)


CODES = _load_code_data()


def country_code(name: str) -> str:
    """Get two letter country code based on name"""
    if not CODES:
        _load_code_data()
    LOGGER.warning(f"Getting country_code for {name}...")
    return CODES.get(name)
