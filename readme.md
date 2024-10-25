# The Wheater Project

**The Weather Project** is a data engineering solution for managing, processing, and storing historical weather data. This repository contains a series of Python-based pipelines that interact with the Meteostat API, download weather data, and store it in a PostgreSQL database. The project is organized to run locally.

## Project Overview

This project leverages data engineering best practices, including data ingestion, processing, and storage. The pipelines are designed to run in a specified order, ensuring that all steps, from initial data setup to incremental loading, are handled efficiently and in the correct sequence.

## Initial Configutation

1. **`src/database/init_db.py`**: Runs initial setup for the PostgreSQL "abyys" database, creating the necessary schemas and tables for storing data.

2. **`Create /.env file`**: Create .env file to store environment variables as following:

DB_CONNECTION_STRING = postgresql+psycopg2://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/abyss
DB_USER = <user name>
DB_PASSWORD = <user password>
DB_HOST = <database host>
DB_PORT = <database port>
DB_NAME = "abyss"
SERVER_DB_NAME = <default database of the server e.g "postgres">

## Order of Execution

The following pipelines should be executed in the specified order to ensure proper orchestration:

1. **`src/pipelines/meteostat_stations_pipeline.py`**: Fetches stations from meteostat API and stores them into raw_meteostat.stations table. It's a full-refresh process.

2. **`src/pipelines/meteostat_hourly_weather_measurements_pipeline.py`**: Fetches hourly weather measurements from the Meteostat API, processes the data, and inserts it into the raw_meteostat.meteostat_hourly_weather_measurements table. This pipeline uses a control table to determine the last ingested timestamp for each station, allowing for incremental data loading.