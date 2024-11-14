FROM apache/airflow:2.10.3

# Copy the requirements file from the host to the Docker image
COPY ./requirements.txt /opt/airflow/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt