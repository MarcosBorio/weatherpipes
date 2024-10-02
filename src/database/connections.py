import psycopg2
from sqlalchemy import create_engine

def create_server_connection(db_name, db_user, db_password, db_host, db_port):
    """
    Create and returns una conexión al servidor PostgreSQL

    :param db_name: Nombre de 
    """
    conn = None
    try:
        conn = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print(f"Conexión exitosa al servidor de la base de datos: {db_name}")
    except Exception as e:
        print(f"Error creating connection object: {e}")
        raise RuntimeError(f"Error in function create_server_connection: {e}")
    return conn


def create_engine_connection(conn_str):
    """
    Crea y devuelve un objeto engine para conectar a la base de datos.

    :param conn_str: Cadena de conexión a la base de datos
    :return: Objeto engine de SQLAlchemy
    """
    try:
        engine = create_engine(conn_str)
    except Exception as e:
        print(f"Error creating engine object: {e}")
        raise RuntimeError(f"Error in function create_engine_connection: {e}")
    return engine

