# pylint: disable=logging-format-interpolation
import json
import logging
import os
from pathlib import Path
from pprint import pformat as pf

import pandas as pd

ROOT = Path(__file__).joinpath("..").joinpath("..").resolve()

LOGGER = logging.getLogger(__name__)

COUNTRY_CODE_DATASET = os.environ.get("COUNTRY_CODE_DATASET", "COUNTRY_CODES.json")
LOGGER.warning("LOADING COUNTRY CODE DATA...")
with open(str(ROOT / "data" / COUNTRY_CODE_DATASET)) as rfile:
    CODES = json.load(rfile)


def json_loader(file_path: Path):
    with open(str(file_path)) as rfile:
        return json.load(rfile)


def country_code(name: str) -> str:
    """Get two letter country code based on name"""
    LOGGER.warning(f"Getting country_code for {name}...")
    return CODES.get(name.lower())


def merge_two_columns_into_dict(file_name: str = "country_to_country_code.csv"):
    """Merge two column CSV file into k: v pairs"""
    df = pd.read_csv(str(ROOT / "data" / file_name), names=["Col1", "Col2"])
    LOGGER.warning(f"First few lines:\n{pf(df.head())}")
    d = df.groupby("Col1")["Col2"].apply(list)
    d = {k: v[0] for k, v in d.items()}
    LOGGER.warning(f"converted json: {pf(d)}")
    return d


def map_wit_unwit_to_cc(unwit_to_wit: str, unwit_to_cc: str):
    """Map dataset"""
    # pylint: disable=import-outside-toplevel,cyclic-import
    from scripts import get_wit

    unwit_to_cc_dict = json_loader((ROOT / "data" / f"{unwit_to_cc}.json"))
    unwit_to_wit_dict = json_loader((ROOT / "data" / f"{unwit_to_wit}.json"))
    LOGGER.warning(f"unwit_to cc data:\n{pf(unwit_to_cc_dict)}")

    if unwit_to_wit_dict == {}:
        unwit_to_wit_dict = get_wit.get_wit(list(unwit_to_cc_dict.keys()))

    wit_to_cc_dict = {}

    for unwit, wit in unwit_to_wit_dict.items():
        country_code = unwit_to_cc_dict.get(unwit)
        if country_code:
            wit_to_cc_dict[wit] = country_code

    LOGGER.warning(f"Results: {pf(wit_to_cc_dict)}")
    return wit_to_cc_dict


def merge_wit_unwit(unwit_to_cc: str, wit_to_cc: str):
    """Merege dataset"""
    data_path = ROOT / "data"
    unwit_to_cc = json_loader((data_path / f"{unwit_to_cc}.json"))
    wit_to_cc = json_loader((data_path / f"{wit_to_cc}.json"))
    unwit_to_cc = {k.lower(): v for k, v in unwit_to_cc.items()}
    wit_to_cc = {k.lower(): v for k, v in wit_to_cc.items()}
    return {**unwit_to_cc, **wit_to_cc}
