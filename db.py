import os
import sqlalchemy

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
engine = sqlalchemy.create_engine(os.environ["DATABASE_URL"])


def insert_db(df, table_name, if_exists="append"):
    """Writes dataframe df to table table_name using the imported
    SQLAlchemy engine.

    """
    df.to_sql(table_name, con=engine, if_exists=if_exists, method='multi')
