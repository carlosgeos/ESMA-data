import os
from filestore import download_file, write_csv, clean_file
from parser import parse_non_equity, parse_equity
from api import get_metadata
from db import insert_db

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = "/tmp/"
HOST_STAGING_DIR = os.environ["HOST_STAGING_DIR"]


def extract(instr_list, output_table):
    for instrument in instr_list:
        xml_file = download_file(instrument, TMP_DIR)
        if instrument["instrument_type"] == "Non-Equity Instruments":
            df = parse_non_equity(instrument, xml_file)
        else:
            df = parse_equity(instrument, xml_file)
        print("Writing CSV...")
        csv_file = f"{HOST_STAGING_DIR}{instrument['file_name'][:-4]}.csv"
        write_csv(df, csv_file)
        print("COPYing to db...")
        insert_db(csv_file, "raw", output_table)
        clean_file(xml_file)
        clean_file(csv_file)
        print(f"Done {xml_file}")


if __name__ == '__main__':
    metadata = get_metadata()

    non_equity_full = list(filter(lambda x: x["instrument_type"] == "Non-Equity Instruments" and x["file_type"] == "Full", metadata))

    equity_full = list(filter(lambda x: x["instrument_type"] == "Equity Instruments" and x["file_type"] == "Full", metadata))

    extract(non_equity_full, "non_equity")
    extract(equity_full, "equity")
