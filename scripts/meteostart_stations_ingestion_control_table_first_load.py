import os
from src.database.query import execute_query
from src.database.insert import insert_dataframe
from dotenv import load_dotenv
from src.database.connections import create_engine_connection

def meteostat_first_load_stations_ingestion_control_table():
    """
    Performs the first load of station IDs into the 'stations_ingestion_control' table.

    Steps:
    1. Load the environment variables and establish the database connection.
    2. Retrieve station IDs from the 'stations' table.
    3. Insert the station IDs into the 'stations_ingestion_control' table.

    :raises RuntimeError: If any errors occur during data insertion.
    """
    try:
        load_dotenv()
        conn_str = os.getenv('DB_CONNECTION_STRING')
        engine = create_engine_connection(conn_str)

        # Fetch all station IDs from the 'stations' table
        stationids = execute_query("SELECT stationid FROM raw_meteostat.stations", engine)

        # Insert station IDs into the 'stations_ingestion_control' table
        insert_dataframe(stationids, "raw_meteostat", "stations_ingestion_control", engine)

    except Exception as e:
        print(f"Error inserting initial data into raw_meteostat.stations_ingestion_control: {e}")
        raise RuntimeError(f"Error in function meteostat_first_load_stations_ingestion_control_table: {e}")