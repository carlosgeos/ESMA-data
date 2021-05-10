import os
import ntpath
import sqlalchemy


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
engine = sqlalchemy.create_engine(os.environ["DATABASE_URL"])
CONTAINER_STAGING_DIR = os.environ["CONTAINER_STAGING_DIR"]


def insert_db(file_name, schema, table):
    """Writes the CSV file named file_name to `schema.table`

    """
    file_to_copy = os.path.join(CONTAINER_STAGING_DIR, ntpath.basename(file_name))
    with open(f"{BASE_PATH}/sql/copy.sql", "r") as sql_file:
        query = sqlalchemy.text(sql_file.read()
                                .replace("<<schema>>", schema)
                                .replace("<<file>>", file_to_copy)
                                .replace("<<tablename>>", table))
        print(query)

        with engine.connect().execution_options(autocommit=True) as conn:
            conn.execute(query)
