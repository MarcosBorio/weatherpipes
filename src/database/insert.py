from src.database.query import execute_query
import pandas as pd
from sqlalchemy import text

def insert_dataframe(dataframe, target_schema, target_table, engine=None, chunk_size=None, if_exists='append', method = None):
    """
    Inserts a pandas DataFrame into a specified database table. The data can be inserted in chunks if chunk_size is specified.

    :param dataframe: pandas DataFrame containing the data to be inserted.
    :param target_schema: Database schema where the table resides.
    :param target_table: Target database table for data insertion.
    :param engine: SQLAlchemy engine object for database connection.
    :param chunk_size: If specified, the data will be inserted in chunks of this size. 
                       If None, the entire DataFrame will be inserted at once.
    :param if_exists: Specifies how to behave if the table already exists ('append', 'replace', etc.).
    
    :raises RuntimeError: If there is an error during the data insertion process.
    """
    try:
        if chunk_size is None:
            # Insert the entire DataFrame at once
            rows = dataframe.to_sql(target_table, con=engine, schema=target_schema, if_exists=if_exists, index=False)
            print(f"Data inserted into {target_schema}.{target_table} (rows inserted: {rows})")
        else:
            # Insert the DataFrame in chunks of the specified size
            total_rows = len(dataframe)
            print(f"Total rows to insert: {total_rows}")

            for i in range(0, total_rows, chunk_size):
                chunk = dataframe.iloc[i:i + chunk_size]
                print(f"Inserting rows {i+1} to {i + len(chunk)} into {target_schema}.{target_table}")
                chunk.to_sql(target_table, con=engine, schema=target_schema, if_exists=if_exists, index=False)

    except Exception as e:
        # Log the error and raise a RuntimeError for higher-level handling
        print(f"Error inserting data into {target_schema}.{target_table}: {e}")
        raise RuntimeError(f"Error in function insert_dataframe: {e}")