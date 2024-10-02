import pandas as pd

def fetch_data(query,engine):
    """
    Returns a dataframe regarding the given SQL query parameter

    :param query: SQL query
    :param engine: Engine object to connect to.

    :return: Pandas dataframe Object  
    """
    try:
        return pd.read_sql(query,engine)
    except Exception as e:
        print(f"Error executing the query: {e}")
        raise RuntimeError(f"Error in function fetch_data: {e}")
