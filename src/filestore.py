import os
import tempfile
import requests as r
import zipfile


def download_file(metadata, path="/tmp/"):
    """Downloads and unzips the downloaded data to `path`. The ZIP files
    are not stored, just uncompressed data

    The metadata arg is a vector of dicts that contain file_type,
    instrument_type and download link among other things

    """
    res = r.get(metadata["download_link"], stream=True)
    extracted = ""
    with tempfile.NamedTemporaryFile() as tmp:
        for chunk in res.iter_content(chunk_size=128):
            tmp.write(chunk)

        with zipfile.ZipFile(tmp, 'r') as zip_ref:
            contents = zip_ref.namelist()
            zip_ref.extractall(path)
            extracted = os.path.join(path, contents[0])

    return extracted


def write_csv(df, file_name):
    """Writes Pandas dataframe df to file_name, with no index column

    """
    df.to_csv(file_name, index=False)


def clean_file(file_name):
    print(f"Removing {file_name}")
    if os.path.exists(file_name):
        os.remove(file_name)
    else:
        print("The file does not exist")
