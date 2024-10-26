# WeatherPipes

WeatherPipes is a data processing module designed as part of The Weather Project to manage and automate pipelines for climate and marine data. Its goal is to centralize and optimize the extraction, transformation, and loading of data from various APIs, including those providing climate information, primary productivity, and species sightings. WeatherPipes facilitates the orchestration of these pipelines, running them on a scheduled or real-time basis, ensuring that data in the project’s PostgreSQL database is consistently updated and accurate.

## Initial Configutation

1. **`src/database/init_db.py`**: Runs initial setup for the PostgreSQL "abyys" database, creating the necessary schemas and tables for storing data.

2. **`Create /.env file`**: Create .env file to store environment variables as following:

```
DB_CONNECTION_STRING = postgresql+psycopg2://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/abyss
DB_USER = <user name>
DB_PASSWORD = <user password>
DB_HOST = <database host>
DB_PORT = <database port>
DB_NAME = "abyss"
SERVER_DB_NAME = <default database of the server e.g "postgres">
```

## Order of Execution

The following pipelines should be executed in the specified order to ensure proper orchestration:

1. **`src/pipelines/meteostat_stations_pipeline.py`**: Fetches stations from meteostat API and stores them into raw_meteostat.stations table. It's a full-refresh process.

2. **`src/pipelines/meteostat_hourly_weather_measurements_pipeline.py`**: Fetches hourly weather measurements from the Meteostat API, processes the data, and inserts it into the raw_meteostat.meteostat_hourly_weather_measurements table. This pipeline uses a control table to determine the last ingested timestamp for each station, allowing for incremental data loading.

## Current Version

The current stable version of WeatherPipes is **v1.0.0**. 

## Roadmap

The following features are planned for future releases:

1. **Orchestration and Scheduling**:
   - Integration with Apache Airflow for automated pipeline scheduling.
   - Implementation of notification systems for pipeline failures or delays.

2. **Extended Data Sources**:
   - Integration with additional climate and marine data APIs.
   - Fetching real-time species sightings data from marine biology databases.