from src.utils.generate_hash import generate_hash

def meteostat_hourly_weather_measurements_processor(raw_data):
    """
    Processes raw hourly weather data fetched from Meteostat.

    Steps:
    1. Reset the index to convert 'station' and 'time' from index to columns.
    2. Add a 'source' column to identify the data source.
    3. Generate a unique hash ('hourlyweathermeasurementid') for each record.
    4. Reorganize the columns for database insertion.

    :param raw_data: pandas DataFrame containing raw hourly weather data.
    :return: Processed DataFrame ready for insertion into the database.
    :raises RuntimeError: If any errors occur during data processing.
    """
    try:
        # Reset the index to convert 'station' and 'time' from index to columns
        raw_data = raw_data.reset_index()

        # Add a column to track the data source
        raw_data['source'] = 'Meteostat'

        # Generate a unique ID for each weather record
        raw_data['hourlyweathermeasurementid'] = raw_data.apply(generate_hash, axis=1, columns={'stationid', 'time'})

        # Reorder columns for consistency before insertion
        raw_data = raw_data[['hourlyweathermeasurementid', 'stationid', 'time', 'temp', 'rhum', 'prcp', 
                             'wdir', 'wspd', 'wpgt', 'pres', 'source']]

    except Exception as e:
        print(f"Error processing hourly measurements from Meteostat: {e}")
        raise RuntimeError(f"Error in function meteostat_hourly_weather_measurements_processor: {e}")

    return raw_data
