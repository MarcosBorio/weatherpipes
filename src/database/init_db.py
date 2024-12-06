import psycopg2
import os
import pandas as pd
from psycopg2 import sql
from src.database.connections import create_server_connection
from dotenv import load_dotenv

def create_database(conn, new_db_name):
    """
    Creates a new PostgreSQL database.

    :param conn: psycopg2 connection object to the PostgreSQL server.
    :param new_db_name: Name of the new database to be created.
    :raises: psycopg2.Error if there is an issue executing the SQL command.
    """
    try:
        conn.autocommit = True  # Required to execute CREATE DATABASE outside a transaction
        cursor = conn.cursor()
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))
        print(f"Database {new_db_name} created successfully.")
    except psycopg2.Error as e:
        print(f"Error creating the database: {e}")

def create_schema(conn, new_db_schema):
    """
    Creates a new schema in the PostgreSQL database.

    :param conn: psycopg2 connection object to the database.
    :param new_db_schema: Name of the schema to create.
    :raises: psycopg2.Error if there is an issue executing the SQL command.
    """
    try:
        conn.autocommit = True  # Required for schema creation
        cursor = conn.cursor()
        cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(new_db_schema)))
        print(f"Schema {new_db_schema} created successfully.")
    except psycopg2.Error as e:
        print(f"Error creating schema: {e}")

def create_meteostat_tables(conn):
    """
    Creates the required raw tables in the PostgreSQL database for Meteostat data ingestion.

    Tables created:
    - raw_meteostat.stations: Stores station information.
    - raw_meteostat.hourly_weather_measurements: Stores hourly weather data for each station.
    - raw_meteostat.stations_ingestion_control: Tracks the last ingestion timestamp for each station.

    :param conn: psycopg2 connection object to the database.
    :raises: psycopg2.Error if there is an issue executing the SQL command.
    """
    try:
        # SQL to create stations table
        sql_create_meteostat_stations_table = """
        CREATE TABLE IF NOT EXISTS raw_meteostat.stations (
            stationid VARCHAR(256) PRIMARY KEY,
            stationname VARCHAR(256) NOT NULL,
            country VARCHAR(100),
            region VARCHAR(100),
            wmo VARCHAR(512),
            icao VARCHAR(100),
            latitude DECIMAL(9,6),
            longitude DECIMAL(9,6),
            elevation FLOAT,
            timezone VARCHAR(100),
            source VARCHAR(256)
        );
        """

        # SQL to create hourly weather measurements table
        sql_create_meteostat_hourly_weather_measurements_table = """
        CREATE TABLE IF NOT EXISTS raw_meteostat.hourly_weather_measurements (
            hourlyweathermeasurementid BIGINT PRIMARY KEY,
            stationid VARCHAR(256) NOT NULL,
            time VARCHAR(100) NOT NULL,
            temp FLOAT,
            rhum FLOAT,
            prcp FLOAT,
            wdir FLOAT,
            wspd FLOAT,
            wpgt FLOAT,
            pres FLOAT,
            source VARCHAR(256)
        );
        """

        # SQL to create ingestion control table
        sql_create_stations_ingestion_control_table = """
        CREATE TABLE IF NOT EXISTS raw_meteostat.stations_ingestion_control (
            stationid VARCHAR(256) PRIMARY KEY,
            hourly_max_timestamp TIMESTAMP NOT NULL DEFAULT '1900/01/01 00:00'
        );
        """

        # Execute SQL statements to create the tables
        cursor = conn.cursor()
        cursor.execute(sql_create_meteostat_stations_table)
        print("Table 'stations' created successfully.")
        conn.commit()

        cursor.execute(sql_create_meteostat_hourly_weather_measurements_table)
        print("Table 'hourly_weather_measurements' created successfully.")
        cursor.execute(sql_create_stations_ingestion_control_table)
        print("Table 'stations_ingestion_control' created successfully.")
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")


def create_obis_tables(conn):
    """
    Creates the required raw tables in the PostgreSQL database for OBIS data ingestion.

    Tables created:
    - raw_meteostat.stations: Information of sightings arround stations.

    :param conn: psycopg2 connection object to the database.
    :raises: psycopg2.Error if there is an issue executing the SQL command.
    """
    try:
        # SQL to create sightings table
        sql_creat_obis_sightings_table = """
        CREATE TABLE raw_obis.sightings (
            sightingid VARCHAR(512) NOT NULL PRIMARY KEY,                
            eventDate VARCHAR(512),                           
            year INT,                                      
            month INT,                                     
            day INT,                                       
            scientificName TEXT,                           
            vernacularName VARCHAR(255),                   
            species VARCHAR(255),                          
            genus VARCHAR(255),                            
            family VARCHAR(255),                           
            phylum VARCHAR(255),                           
            kingdom VARCHAR(255),                          
            decimalLatitude DOUBLE PRECISION,              
            decimalLongitude DOUBLE PRECISION,             
            waterBody VARCHAR(255),                        
            locality TEXT,                                 
            country VARCHAR(100),                          
            sst DOUBLE PRECISION,                          
            sss DOUBLE PRECISION,                          
            bathymetry DOUBLE PRECISION,                   
            shoreDistance DOUBLE PRECISION,                
            depth DOUBLE PRECISION,                        
            basisOfRecord TEXT,                            
            coordinateUncertaintyInMeters DOUBLE PRECISION,
            occurrenceStatus VARCHAR(50),                                               
            datasetName TEXT,                              
            scientificNameID VARCHAR(255),
            source VARCHAR(256),
            stationid VARCHAR(256) NOT NULL                
        );
        """
        
        # Execute SQL statements to create the tables
        cursor = conn.cursor()
        cursor.execute(sql_creat_obis_sightings_table)
        print("Table 'sightings' created successfully.")
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")            

def init_db():
    """
    Initializes the database by creating the necessary database, schema, and tables for Meteostat data ingestion.

    Steps:
    1. Load environment variables for database configuration.
    2. Create the database if it doesn't exist.
    3. Create the raw schema and tables required for Meteostat data ingestion.
    
    :raises: RuntimeError if there is an issue with database creation or connection.
    """
    # Load environment variables (e.g., DB credentials)
    load_dotenv()

    # Database configuration
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')  # Name of the database to be created
    server_db_name = os.getenv('SERVER_DB_NAME')  # Existing database for server connection

    # Step 1: Connect to the PostgreSQL server
    server_conn = create_server_connection(server_db_name, db_user, db_password, db_host, db_port)

    # Step 2: Create the database if it doesn't exist
    if server_conn is not None:
        create_database(server_conn, db_name)
        server_conn.close()

    # Step 3: Connect to the newly created database
    conn = create_server_connection(db_name, db_user, db_password, db_host, db_port)

    # Step 4: Create schemas and required tables
    if conn is not None:
        create_schema(conn, 'raw_meteostat')
        create_meteostat_tables(conn)
        create_schema(conn, 'raw_obis')
        create_obis_tables(conn)
        server_conn.close()
        conn.close()  # Close the connection to the database
