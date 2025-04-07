
# SF Fire Incidents Data Pipeline

This project provides a complete data pipeline to ingest, model, and analyze fire incident data from the City of San Francisco. It enables the Business Intelligence team to perform fast, dynamic queries across key dimensions: **time period**, **district**, and **battalion**.

---

## Project Structure

- `load_fire_data.py` — Python script to fetch and load the latest fire incidents data into PostgreSQL.
- `docker-compose.yml` — Spins up PostgreSQL and pgAdmin locally.
- `sf_fire_dbt/` — A dbt project that models the ingested data for BI-friendly analysis.
- `requirements.txt` — Python dependencies for ingestion and dbt setup.

---

## Tech Stack

- Python 3.12
- PostgreSQL (via Docker)
- dbt (v1.9+)
- pandas, SQLAlchemy
- pgAdmin (optional)

---

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Create a virtual environment

```bash
python3 -m venv sf_fire_env
source sf_fire_env/bin/activate
pip install -r requirements.txt
```

### 3. Start the database

```bash
docker-compose up -d
```

- PostgreSQL runs on `localhost:5433`
- pgAdmin is available at http://localhost:9091 (login: `admin@admin.com`, password: `admin`)

### 4. Load the dataset

```bash
python load_fire_data.py
```

This script will download the latest SF Fire Incidents data, normalize column names, and load the data into the PostgreSQL `fire_incidents` table.

---

## dbt Setup & Usage

### 5. Configure dbt profile

Create a file at `~/.dbt/profiles.yml` with the following content:

```yaml
sf_fire_dbt:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: fireuser
      password: firepass
      port: 5433
      dbname: firedata
      schema: public
      threads: 1
```

### 6. Run dbt models

```bash
cd sf_fire_dbt
dbt run
```

This builds:

- `stg_fire_incidents`: staging view from raw data
- `agg_fire_summary`: aggregated view by month, district, and battalion

---

## Example Query

```sql
SELECT *
FROM agg_fire_summary
WHERE month >= '2024-01-01'
  AND district = 'Mission'
ORDER BY month;
```

---

## Assumptions

- The source dataset is updated daily. We overwrite the table each time.
- All columns are normalized to `snake_case`.
- BI queries use `incident_date` for time-based aggregations.
- This solution assumes a local environment using Docker.

---

## Source

Data provided by the [SF Open Data Portal](https://data.sfgov.org/Public-Safety/Fire-Incidents/wr8u-xric)
