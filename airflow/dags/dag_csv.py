#SALVANDO EM CSV - VERSÃO CORRIGIDA

from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
import boto3
import pandas as pd
import io


# ARGUMENTOS PADRÕES DA DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

@dag(
    dag_id='postgres_to_minio_csv',
    default_args=default_args,
    description='Carga Incremental do Postgres para MinIO em csv',
    schedule_interval=timedelta(days=1),
    catchup=False
)
def postgres_to_minio_etl():
    
    table_names = ['veiculos', 'estados', 'cidades', 'concessionarias', 'vendedores', 'clientes', 'vendas']
    
    @task
    def process_table(table_name: str):
        """Processa uma tabela: busca dados do PostgreSQL e salva no MinIO"""
        
        # Inicializar cliente S3
        s3_client = boto3.client(
            's3',
            endpoint_url='http://minio:9000',
            aws_access_key_id='minioadmin',
            aws_secret_access_key='minio123'
        )
        bucket_name = 'landing'
        
        try:
            # 1. Buscar max_id do arquivo anterior (se existir)
            try:
                response = s3_client.get_object(Bucket=bucket_name, Key=f"{table_name}/max_id.txt")
                max_id = int(response['Body'].read().decode('utf-8'))
            except s3_client.exceptions.NoSuchKey:
                max_id = 0
            
            # 2. Conectar ao PostgreSQL e buscar dados
            pg_hook = PostgresHook(postgres_conn_id='postgres')
            pg_conn = pg_hook.get_conn()
            pg_cursor = pg_conn.cursor()
            
            # Obter nomes das colunas
            pg_cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position")
            columns = [row[0] for row in pg_cursor.fetchall()]
            columns_str = ', '.join(columns)
            
            # Obter nome da chave primária
            primary_key = f'id_{table_name}'
            
            # Buscar dados incrementais
            query = f"SELECT {columns_str} FROM {table_name} WHERE {primary_key} > {max_id} ORDER BY {primary_key}"
            pg_cursor.execute(query)
            rows = pg_cursor.fetchall()
            
            pg_cursor.close()
            pg_conn.close()
            
            # 3. Se houver dados, salvar em CSV no MinIO
            if rows:
                df = pd.DataFrame(rows, columns=columns)
                
                # Salvar arquivo CSV
                csv_buffer = df.to_csv(index=False)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=f"{table_name}/data_{timestamp}.csv",
                    Body=csv_buffer
                )
                
                # Atualizar max_id
                new_max_id = df[primary_key].max()
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=f"{table_name}/max_id.txt",
                    Body=str(new_max_id)
                )
                
                return {
                    'table': table_name,
                    'rows_processed': len(df),
                    'max_id': new_max_id,
                    'status': 'success'
                }
            else:
                return {
                    'table': table_name,
                    'rows_processed': 0,
                    'max_id': max_id,
                    'status': 'no_data'
                }
                
        except Exception as e:
            return {
                'table': table_name,
                'status': 'error',
                'error': str(e)
            }
    
    # Processar cada tabela em paralelo
    results = [process_table(table_name) for table_name in table_names]

postgres_to_minio_etl_dag = postgres_to_minio_etl()