import os
import subprocess
from dotenv import load_dotenv
from database.connections import create_server_connection
from database.init_db import create_database

def init_af():
    """
    Initializes the Airflow environment by setting up configurations, creating the metadata database, 
    and starting the necessary Airflow services using Docker Compose. 

    This function is designed to simplify the initialization process by:
    1. Loading environment variables from the `.env` file, which includes database credentials, 
    Airflow home directory, and other configurations.
    2. Creating the Airflow metadata database in PostgreSQL using credentials and a connection to the 
    default server database (`server_db_name`).
    3 Starting the Airflow webserver and scheduler services via Docker Compose.
    """

    try:
        #Step 1 - Load environment variables from .env file
        load_dotenv()
        db_user = os.getenv("DB_USER_AF")
        db_password = os.getenv("DB_PASSWORD_AF")
        db_host = os.getenv("DB_HOST_AF")
        db_port = os.getenv("DB_PORT_AF")
        db_name = os.getenv("DB_NAME_AF")
        server_db_name = os.getenv('SERVER_DB_NAME')  #Existing database for server connection  

        #Step 2 - Create airflow database
        #Connect to the default database
        server_conn = create_server_connection(server_db_name, db_user, db_password, db_host, db_port)

        if server_conn is not None:
            create_database(server_conn, db_name)
        server_conn.close()

        #Step 3 - Start docker compose to create webserver and scheduler services.
        compose_file_path = "./twp_airflow/docker-compose.yml" 
        subprocess.run(["docker-compose", "-f", compose_file_path, "up", "-d"], check=True)
        print("Docker Compose services started successfully.")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")