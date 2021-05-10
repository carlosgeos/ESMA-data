import requests

URL = "https://registers.esma.europa.eu/solr/esma_registers_fitrs_files/select?q=*&fq=creation_date:%5B2017-11-24T00:00:00Z+TO+2021-12-31T23:59:59Z%5D&wt=json&indent=true&start=0&rows=100000"


def get_metadata():
    """Calls the metadata endpoint to get all available files for
    download. Delta + Full for both equity and non-equity instruments

    Returns a vector of items which contain the following information:

    - instrument_type (Non-Equity Instruments or Equity Instruments)
    - download_link
    - id
    - file_type (Delta of Full)

    """
    res = requests.get(URL).json()
    return res["response"]["docs"]
