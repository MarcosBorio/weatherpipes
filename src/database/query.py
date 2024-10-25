import pandas as pd
from sqlalchemy import text

def execute_query(query, engine, is_select=True):
    """
    Executes a given SQL query using the provided SQLAlchemy engine. If it's a SELECT query, the result is returned 
    as a pandas DataFrame. For other queries (INSERT, UPDATE, DELETE), it executes the query directly.

    :param query: The SQL query to execute.
    :param engine: SQLAlchemy engine object to connect to the database.
    :param is_select: Boolean flag indicating whether the query is a SELECT query (True) or another SQL operation (False).
    :return: Pandas DataFrame for SELECT queries or the result of the executed query for non-SELECT operations.
    :raises RuntimeError: If any error occurs during the query execution.
    """
    try:
        if is_select:
            # Execute the SELECT query and return the result as a DataFrame
            result = pd.read_sql(query, engine)
        else:
            # For non-SELECT queries, execute the query within a transaction block
            with engine.connect() as connection:
                with connection.begin():
                    result = connection.execute(text(query))
                    connection.commit()
        #print(f"Query executed: {query}")
        return result

    except Exception as e:
        # Log and raise the error for higher-level handling
        print(f"Error executing the query: {e}")
        raise RuntimeError(f"Error in function execute_query: {e}")
