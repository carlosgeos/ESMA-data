from filestore import download_files
from parser import parse_non_eqty
from api import get_metadata
from db import insert_db


metadata = list(filter(lambda x: x["instrument_type"] == "Non-Equity Instruments", get_metadata()))[:2]

download_files(metadata)

for f in metadata:
    df = parse_non_eqty(f"raw_data/{f['file_name'][:-4]}.xml")
    insert_db(df, "non_eqty")
