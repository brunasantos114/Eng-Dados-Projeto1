from airflow import DAG
# type: ignore
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_spark_job():
    # Conectar ao Spark via HTTP (dentro da rede Docker)
    spark_master_url = "spark://spark:7077"  # Dentro da rede Docker
    
    # Se você quer submeter via REST ou executar um script Python
    # que já existe no volume mapeado
    import subprocess
    result = subprocess.run([
        "python", 
        "/spark_connector/read_data.py"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Erro no Spark: {result.stderr}")
    
    print(result.stdout)

with DAG(
    'dag_landing_lakehouse',
    default_args=default_args,
    description='Carga inicial com Spark salvando no MinIO',
    schedule_interval=timedelta(days=1),
    catchup=False
) as dag:

    run_etl = PythonOperator(
        task_id='carga_landing',
        python_callable=run_spark_job
    )