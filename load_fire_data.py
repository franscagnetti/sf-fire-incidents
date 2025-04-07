import pandas as pd
from sqlalchemy import create_engine, text
import requests
import io

DATA_URL = "https://data.sfgov.org/api/views/wr8u-xric/rows.csv?accessType=DOWNLOAD"

DB_USER = "fireuser"
DB_PASS = "firepass"
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "firedata"
TABLE_NAME = "fire_incidents"

def load_data():
    print("Downloading dataset...")
    response = requests.get(DATA_URL)
    if response.status_code != 200:
        raise Exception("Failed to download dataset")

    df = pd.read_csv(io.StringIO(response.text), low_memory=False)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    print(f"Downloaded {len(df)} rows.")

    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    print(f"Dropping dependent views and table `{TABLE_NAME}`...")
    with engine.connect() as conn:
        conn.execute(text("DROP VIEW IF EXISTS stg_fire_incidents CASCADE;"))
        conn.execute(text(f"DROP TABLE IF EXISTS {TABLE_NAME} CASCADE;"))

    print(f"Loading data into PostgreSQL table `{TABLE_NAME}`...")
    df.to_sql(TABLE_NAME, engine, index=False)
    print("Data loaded successfully.")

if __name__ == "__main__":
    load_data()

