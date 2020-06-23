# pylint: disable=logging-format-interpolation
import json
import logging
from pathlib import Path
from pprint import pformat as pf

import pandas as pd

ROOT = Path(__file__).joinpath("..").joinpath("..").resolve()

LOGGER = logging.getLogger(__name__)


LOGGER.warning("LOADING COUNTRY CODE DATA...")
with open(str(ROOT / "data" / "country_codes_temp.json")) as rfile:
    CODES = json.load(rfile)


def country_code(name: str) -> str:
    """Get two letter country code based on name"""
    LOGGER.warning(f"Getting country_code for {name}...")
    return CODES.get(name)


def merge_two_columns_into_dict(file_name: str = "country_to_country_code.csv"):
    """Merge two column CSV file into k: v pairs"""
    df = pd.read_csv(str(ROOT / "data" / file_name), names=["Col1", "Col2"])
    LOGGER.warning(f"First few lines:\n{pf(df.head())}")
    d = df.groupby("Col1")["Col2"].apply(list)
    d = {k: v[0] for k, v in d.items()}
    LOGGER.warning(f"converted json: {pf(json.dumps(d))}")
    return d
