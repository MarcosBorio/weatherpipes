import os
from meteostat import Stations
from sqlalchemy import create_engine
from src.database.insert import insert_dataframe
from scripts.meteostat_stations_processor import meteostat_stations_processor
from dotenv import load_dotenv

def meteostat_stations_pipeline():
    """
    Pipeline to retrieve and process weather stations data from Meteostat.

    Steps:
    1. Load environment variables and establish the database connection.
    2. Fetch stations data that provide hourly historical information.
    3. Process the raw station data.
    4. Insert processed station data into the database, replacing any existing records.

    :raises RuntimeError: If any errors occur during the pipeline execution.
    """
    try:
        load_dotenv()
        conn_str = os.getenv('DB_CONNECTION_STRING')

        # Step 1 - Retrieve stations data from Meteostat (only those with hourly data)
        stations = Stations()
        stations = stations.inventory('hourly')
        raw_data = stations.fetch()

        # Step 2 - Process the raw station data
        processed_data = meteostat_stations_processor(raw_data)

        # Step 3 - Insert processed data into the 'stations' table (replace existing data)
        engine = create_engine(conn_str)
        insert_dataframe(dataframe=processed_data, target_schema='raw_meteostat', 
                         target_table='stations', engine=engine, if_exists='replace')

    except Exception as e:
        print(f"Error in function meteostat_stations_pipeline: {e}")
        raise RuntimeError(f"Error in function meteostat_stations_pipeline: {e}")

    finally:
        # Ensure the connection is closed properly
        engine.dispose()
        print(f"Connections closed successfully")
