# WeatherPipes

WeatherPipes is a data processing module designed as part of The Weather Project to manage and automate pipelines for climate and marine data. Its goal is to centralize and optimize the extraction, transformation, and loading of data from various APIs, including those providing climate information, primary productivity, and species sightings. WeatherPipes facilitates the orchestration of these pipelines, running them on a scheduled or real-time basis, ensuring that data in the project’s PostgreSQL database is consistently updated and accurate.

## Prerequisites

Before proceeding with the setup, ensure the following requirements are met:

### Docker and Docker Compose

1. **Install Docker**:  
   Go to the official Docker website and download the Docker Desktop for your operating system. 
   Follow the installation instructions provided on the Docker website. Start docker service.

## Initial Configuration

1. **`Create /.env file`**: Create and set /.env file based on /.env.example file

2. **`src/database/init_db.py`**: Runs initial setup for the PostgreSQL "abyys" database, creating the necessary schemas and tables for storing data. Note: Create "abyys" database users and privileges after inicialization.

3. **`airflow/init_af.py`**: Initializes Airflow envirnoment by setting up initial configurations and creating a persistent metadata database in postgres. The function also starts airflow scheduler and webserver (8080) services. Note: Create airflow database users and privileges after inicialization (airflow database = ${DB_NAME_AF} env variable)

## Order of pipelines execution

The following pipelines should be executed in the specified order to ensure proper orchestration:

1. **`src/pipelines/meteostat_stations_pipeline.py`**: Fetches stations from meteostat API and stores them into raw_meteostat.stations table. It's a full-refresh process.

2. **`src/pipelines/meteostat_hourly_weather_measurements_pipeline.py`**: Fetches hourly weather measurements from the Meteostat API, processes the data, and inserts it into the raw_meteostat.meteostat_hourly_weather_measurements table. This pipeline uses a control table to determine the last ingested timestamp for each station, allowing for incremental data loading.

## Current Version

The current stable version of WeatherPipes is tag **v1.0.1**.

## Roadmap

The following features are planned for future releases:

1. **Orchestration and Scheduling**:
   - Implementation of notification systems for pipeline failures or delays.

2. **Extended Data Sources**:
   - Integration with additional climate and marine data APIs.
   - Fetching real-time species sightings data from marine biology databases.