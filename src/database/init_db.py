import psycopg2
import os
from psycopg2 import sql
from src.database.connections import create_server_connection
from dotenv import load_dotenv

def create_database(conn, new_db_name):
    """Crea una nueva base de datos"""
    try:
        conn.autocommit = True  #Necesario para poder ejecutar CREATE DATABASE
        cursor = conn.cursor()
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(new_db_name))
        )
        print(f"Base de datos {new_db_name} creada exitosamente.")
    except psycopg2.Error as e:
        print(f"Error al crear la base de datos: {e}")

def create_schema(conn, new_db_schema):
    """Crea un nuevo schema"""
    try:
        conn.autocommit = True  # Necesario para poder ejecutar CREATE DATABASE
        cursor = conn.cursor()
        cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
            sql.Identifier(new_db_schema))
        )
        print(f"Schema {new_db_schema} creado exitosamente")
    except psycopg2.Error as e:
        print(f"Error al crear el esquema: {e}")        

def create_meteostat_raw_tables(conn):
    """Crea las tablas raw en la base de datos"""
    try:
        sql_create_stations_table = """
        CREATE TABLE IF NOT EXISTS raw_meteostat.stations (
            stationid VARCHAR(256) PRIMARY KEY,
            stationname VARCHAR(256) NOT NULL,
            country VARCHAR(100),
            region VARCHAR(100),
            wmo VARCHAR(512),
            icao VARCHAR(100),
            latitude DECIMAL(9,6),
            longitude DECIMAL(9,6),
            elevation float,
            timezone VARCHAR(100),
            source VARCHAR(256)
        );
        """

        sql_create_hourly_weather_measurements_table = """
        CREATE TABLE IF NOT EXISTS raw_meteostat.hourly_weather_measurements (
            hourlyweathermeasurementid BIGINT PRIMARY KEY,
            stationid VARCHAR(256) NOT NULL,
            time VARCHAR(100) NOT NULL,
            temp float,
            rhum float,
            prcp float,
            wdir float,
            wspd float,
            wpgt float,
            pres float,
            source VARCHAR(256)
        );
        """
        cursor = conn.cursor()
        cursor.execute(sql_create_stations_table)
        print("Tabla 'stations' creada exitosamente.")
        conn.commit()
        cursor.execute(sql_create_hourly_weather_measurements_table)
        print("Tabla 'hourly_weather_measurements' creada exitosamente.")
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error al crear la tabla: {e}")

def init_db():
    #Cargar las variables de entorno desde el archivo .env
    load_dotenv()

    # Configuración de la base de datos
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME') # Nombre de la nueva base de datos a crear
    server_db_name = os.getenv('SERVER_DB_NAME')  # Base de datos existente para conectarse al servidor

    # Paso 1: Conectar al servidor PostgreSQL
    server_conn = create_server_connection(server_db_name, db_user, db_password, db_host, db_port)

    # Paso 2: Crear la base de datos si no existe
    if server_conn is not None:
        create_database(server_conn, db_name)
        server_conn.close()  # Cerrar la conexión al servidor

    # Paso 3: Conectar a la nueva base de datos
    conn = create_server_connection(db_name, db_user, db_password, db_host, db_port)

    # Paso 4:Crear esquema y tablas
    if conn is not None:
        create_schema(conn,'raw_meteostat')    
        create_meteostat_raw_tables(conn)
        server_conn.close() 
        conn.close()  # Cerrar la conexión a la base de datos