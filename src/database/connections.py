import psycopg2
from sqlalchemy import create_engine

def create_server_connection(db_name, db_user, db_password, db_host, db_port):
    """
    Establishes a direct connection to a PostgreSQL database using psycopg2.

    :param db_name: Name of the PostgreSQL database.
    :param db_user: Username for the database connection.
    :param db_password: Password for the database user.
    :param db_host: Host address of the database.
    :param db_port: Port number for the PostgreSQL server.
    :return: psycopg2 connection object to the PostgreSQL server.
    
    :raises RuntimeError: If an error occurs while establishing the connection.
    """
    conn = None
    try:
        # Establish connection using psycopg2
        conn = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print(f"Successfully connected to the database: {db_name}")
    except Exception as e:
        # Log the error and raise a RuntimeError for higher-level handling
        print(f"Error creating connection object: {e}")
        raise RuntimeError(f"Error in function create_server_connection: {e}")
    
    return conn


def create_engine_connection(conn_str):
    """
    Creates and returns an SQLAlchemy engine object for database interaction.

    :param conn_str: Database connection string, typically in the format 
                     'dialect+driver://username:password@host:port/database'.
    :return: SQLAlchemy engine object for executing SQL queries and managing database connections.
    
    :raises RuntimeError: If an error occurs while creating the engine object.
    """
    try:
        # Create an SQLAlchemy engine for database interactions
        engine = create_engine(conn_str)
    except Exception as e:
        # Log the error and raise a RuntimeError for higher-level handling
        print(f"Error creating engine object: {e}")
        raise RuntimeError(f"Error in function create_engine_connection: {e}")
    
    return engine
