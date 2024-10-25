def meteostat_stations_processor(raw_data):
    """
    Processes raw station data retrieved from Meteostat.

    Steps:
    1. Filters out stations with elevation above 0 meters (focus on sea-level stations).
    2. Resets the index to ensure consistent structure.
    3. Adds a 'source' column to identify the origin of the data.
    4. Renames columns to match the database schema.
    5. Reorganizes the columns for consistent database insertion.

    :param raw_data: pandas DataFrame containing the raw station data.
    :return: Processed DataFrame ready for insertion into the database.
    :raises RuntimeError: If any errors occur during the data processing.
    """
    
    try:
        # Filter stations that are at sea level (elevation = 0)
        raw_data = raw_data[raw_data['elevation'] == 0]

        # Reset the index for consistent data structure
        raw_data = raw_data.reset_index()

        # Add a column to track the data source
        raw_data['source'] = 'Meteostat'

        # Rename columns to align with the database schema
        raw_data.rename(columns={'id': 'stationid', 'name': 'stationname'}, inplace=True)

        # Reorganize columns for database insertion
        processed_data = raw_data[['stationid', 'stationname', 'country', 'region', 'wmo', 'icao',
                                   'latitude', 'longitude', 'elevation', 'timezone', 'source']]

        print("Raw station data processed successfully")
        
    except Exception as e:
        # Print the error and raise a RuntimeError for higher-level handling
        print(f"Error processing stations from meteostat: {e}")
        raise RuntimeError(f"Error in function meteostat_stations_processor: {e}")
    
    return processed_data
