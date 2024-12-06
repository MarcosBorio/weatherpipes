import os
import pandas as pd
from datetime import datetime
from src.database.connections import create_engine_connection
from src.database.query import execute_query
from meteostat import Hourly
from scripts.meteostat_hourly_weather_measurements_processor import meteostat_hourly_weather_measurements_processor
from src.database.insert import insert_dataframe
from dotenv import load_dotenv

def meteostat_hourly_weather_measurements_pipeline():
    """
    Pipeline to retrieve, process, and store hourly weather measurements from Meteostat.

    Steps:
    1. Connect to the database using environment variables.
    2. Fetch station IDs from the 'stations' table.
    3. For each station, insert a control record if it doesn't exist.
    4. Retrieve the latest timestamp for the station and fetch new weather data from the Meteostat API.
    5. Process the raw data and insert the results into the 'hourly_weather_measurements' table.
    6. Update the control table with the latest timestamp.

    :raises RuntimeError: If any errors occur during the pipeline execution.
    """
    try:
        load_dotenv()
        conn_str = os.getenv('DB_CONNECTION_STRING')

        # Step 1 - Establish connection to the database
        engine = create_engine_connection(conn_str)

        # Step 2 - Fetch station IDs
        query = 'SELECT stationid FROM raw_meteostat.stations'
        stations = execute_query(query, engine)
        
        # Step 3 - Process each station
        for i in stations.itertuples(name='station'):
            stationid = i[1]

            # Insert station control record if it doesn't exist
            query = '''INSERT INTO raw_meteostat.stations_ingestion_control (stationid) 
                       VALUES ('{}') ON CONFLICT (stationid) DO NOTHING;'''.format(stationid)
            execute_query(query, engine, is_select=False)

            #  Update the control table with the latest timestamp
            query = '''UPDATE raw_meteostat.stations_ingestion_control
                       SET hourly_max_timestamp = COALESCE(
                           (SELECT MAX(m.time)::timestamp 
                            FROM raw_meteostat.hourly_weather_measurements m 
                            WHERE m.stationid = stations_ingestion_control.stationid), 
                           hourly_max_timestamp) 
                       WHERE stationid = '{}' '''.format(stationid)
            execute_query(query, engine, is_select=False)

            # Retrieve the latest timestamp and calculate the start time for new data fetch
            query = """SELECT hourly_max_timestamp::timestamp + INTERVAL '1 hour' 
                       AS hourly_max_timestamp FROM raw_meteostat.stations_ingestion_control 
                       WHERE stationid = '{}' LIMIT 1""".format(stationid)
            start_datetime = pd.to_datetime(execute_query(query, engine)["hourly_max_timestamp"].values[0])
            end_datetime = datetime.utcnow()

            # Fetch raw data from Meteostat API
            raw_data = Hourly(stationid, start=start_datetime, end=end_datetime).fetch()
            raw_data['stationid'] = stationid

            # Process and insert data
            processed_data = meteostat_hourly_weather_measurements_processor(raw_data)
            insert_dataframe(dataframe=processed_data, target_schema='raw_meteostat', 
                             target_table='hourly_weather_measurements', engine=engine, 
                             chunk_size=10000, if_exists='append')
            
    except Exception as e:
        print(f"Error in function meteostat_hourly_weather_measurements_pipeline: {e}")
        raise RuntimeError(f"Error in function meteostat_hourly_weather_measurements_pipeline: {e}")

    finally:
        # Ensure the connection is closed properly
        engine.dispose()
        print(f"Connections closed successfully")
