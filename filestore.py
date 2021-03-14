import tempfile
import requests as r
import zipfile


def download_files(metadata, path="raw_data/"):
    """Downloads and unzips the downloaded data to `path`. The ZIP files
    are not stored, just uncompressed data

    The metadata arg is a vector of dicts that contain file_type,
    instrument_type and download link among other things

    """
    for item in metadata:
        res = r.get(item["download_link"], stream=True)

        with tempfile.NamedTemporaryFile() as tmp:
            for chunk in res.iter_content(chunk_size=128):
                tmp.write(chunk)

            with zipfile.ZipFile(tmp, 'r') as zip_ref:
                zip_ref.extractall(path)


def write_csv(df, file_name):
    df.to_csv(f"csv/{file_name}.csv", index=False)
