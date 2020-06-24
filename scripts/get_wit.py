# pylint: disable=logging-format-interpolation
import json
import logging
from pathlib import Path

from api.utils import WIT_CLIENT, handle_location
from models import wit

LOGGER = logging.getLogger(__name__)

ROOT = Path(__file__).joinpath("..").joinpath("..").resolve()

# Remeber to add {United Kingdom: GB}


def get_wit(countries=None):
    if not countries:
        with open(str(ROOT / "data" / "unwit_country_names.json")) as rfile:
            countries = json.load(rfile)

    name_to_wit = {}

    for country in countries:
        LOGGER.warning(f"extracting {country}")
        meaning = wit.TextMeaning.parse_obj(WIT_CLIENT.message(country))
        _, resolved_lists = handle_location(meaning)
        wit_country_name = resolved_lists[0] if resolved_lists else None
        LOGGER.warning(f"{country}: resolved from Wit {wit_country_name}")
        if wit_country_name:
            name_to_wit.update({country: wit_country_name.lower()})
        else:
            name_to_wit.update({country: country.lower()})

    LOGGER.warning("Dumping to file...")
    with open(str(ROOT / "data" / "unwit_to_wit_countries.json"), "w") as outfile:
        json.dump(name_to_wit, outfile)

    return name_to_wit
