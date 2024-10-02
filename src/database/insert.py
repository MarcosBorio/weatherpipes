def insert_dataframe(dataframe, target_schema='raw_meteostat', target_table='hourly_weather_measurements', engine=None, chunk_size=None):
    """
    Inserta un DataFrame en la tabla objetivo. Si se especifica chunk_size, inserta los datos por bloques de tamaño chunk_size.
    
    :param dataframe: DataFrame con los datos a insertar.
    :param target_schema: Esquema de la base de datos donde insertar los datos.
    :param target_table: Tabla de la base de datos donde insertar los datos.
    :param engine: Conexión activa a la base de datos.
    :param chunk_size: Tamaño del bloque de datos a insertar. Si es None, inserta todo el DataFrame de una vez.
    """
    try:
        if chunk_size is None:
            # Inserta todo el DataFrame de una vez
            rows = dataframe.to_sql(target_table, con=engine, schema=target_schema, if_exists='append', index=False) 
            print(f"Data inserted into table {target_schema}.{target_table} (rows = {rows})")
        else:
            # Inserta el DataFrame en bloques de tamaño chunk_size
            total_rows = len(dataframe)
            print(f"Total de registros a insertar: {total_rows}")

            for i in range(0, total_rows, chunk_size):
                chunk = dataframe.iloc[i:i + chunk_size]
                print(f"Insertando registros {i} a {i + len(chunk) - 1} en la tabla {target_schema}.{target_table}")
                chunk.to_sql(target_table, con=engine, schema=target_schema, if_exists='append', index=False)

    except Exception as e:
        print(f"Error al insertar datos en la tabla {target_schema}.{target_table}: {e}")
        raise RuntimeError(f"Error in function insert_dataframe: {e}")