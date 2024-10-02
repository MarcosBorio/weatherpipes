import hashlib

def generate_hash(row, columns):
    try:
        # Concatenar los valores de las columnas especificadas y codificar la cadena
        hash_input = '_'.join([str(row[col]) for col in columns]).encode()
    
        # Generar un hash usando SHA-256 y convertirlo a un número entero
        hash_object = hashlib.sha256(hash_input)
        hash_value = int(hash_object.hexdigest(), 16) % (15**15)
                
    except Exception as e:
        print(f"Error in generating hash for columns {columns}")    
        raise RuntimeError(f"Error in function generate_hash: {e}")
    return  hash_value 
