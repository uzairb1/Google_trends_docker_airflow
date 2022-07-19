from airflow.models import DAG# type: ignore
from airflow.operators.python_operator import PythonOperator# type: ignore
from airflow.utils.dates import days_ago# type: ignore
from scripts.get_trends import run
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator# type: ignore

args = {
    'owner': 'Uzair Bhatti',
    'start_date': days_ago(1) # make start date in the past
}


#defining the dag object
dag = DAG(
    dag_id='Trends',
    default_args=args,
    schedule_interval='@daily' #to make this workflow happen every day
)

#assigning the task for our dag to do
with dag:
    get_trends = PythonOperator(
        task_id='get_trends_to_gcs',
        python_callable=run,
        # provide_context=True
    )
    load_data = GCSToBigQueryOperator(
    task_id='gcs_to_bigquery',
    bucket='keys_data_786_123',
    source_objects=['keys_data_786_123/keys_data_786_123/airflow.csv'],
    destination_project_dataset_table=f"Trends.airflow.csv",
    autodetect=True,
    write_disposition='WRITE_TRUNCATE',
    dag=dag
    )
    get_trends>>load_data