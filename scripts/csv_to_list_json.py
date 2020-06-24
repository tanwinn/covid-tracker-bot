import json
from pathlib import Path

ROOT = Path(__file__).joinpath("..").joinpath("..").resolve()
with open(str(ROOT / "resources" / "unwit_country_names.csv")) as rfile:
    result = [line.rstrip("\n") for line in rfile]
with open(str(ROOT / "data" / "unwit_country_names.json"), "w") as outfile:
    json.dump(result, outfile)
