import hashlib

def generate_hash(row, columns):
    """
    Generates a hash based on the values of the specified columns in a row. The function uses the SHA-256 hashing algorithm 
    to create a unique integer value for each row.

    :param row: A row of data, typically passed from a pandas DataFrame.
    :param columns: A list of column names whose values will be concatenated to generate the hash.
    :return: An integer hash value derived from the specified columns.
    :raises RuntimeError: If any error occurs during the hash generation process.
    """
    try:
        # Concatenate the values of the specified columns, separated by underscores, and encode the string
        hash_input = '_'.join([str(row[col]) for col in columns]).encode()

        # Generate a SHA-256 hash and convert it to an integer value
        hash_object = hashlib.sha256(hash_input)
        hash_value = int(hash_object.hexdigest(), 16) % (15**15)  # Use modulo to limit hash size

    except Exception as e:
        # Log and raise an error if hash generation fails
        print(f"Error in generating hash for columns {columns}")
        raise RuntimeError(f"Error in function generate_hash: {e}")

    return hash_value
