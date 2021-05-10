# ESMA Register file scraper

This tool is designed to download, parse and transform data from ESMA's Financial Instruments Transparency System (FITRS).

As Directive 2014/65/EU (MiFID II/MiFIR) stipulates, equity-like instruments should carry information such as standard market size and most relevant market (in terms of liquidity).

All of these fields are contained in the zipped XML files provided by ESMA.

Because XML is not great format to run analysis on, this tool extracts, parses and outputs CSV files, with all the relevant fields, which are then `COPY`ed to a Postgres DB.

## Usage

```
$ pipenv install
$ pipenv shell
$ python src/main.py
```

## ENV vars

`DATABASE_URL`, `HOST_STAGING_DIR` (where the output CSV files should be copied, from the Python process point of view) and `CONTAINER_STAGING_DIR` (where the CSV files are located, from the Postgres container/instance point of view).

If a Docker container is not used to spin up Postgres, then the latter is not necessary and is simply the same as `HOST_STAGING_DIR`.

## Data volume

Full (not Delta) files, equity-like data is about 11M rows and non-equity around 1,5B.
