from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'kubernetes_sample', default_args=default_args, schedule_interval=timedelta(minutes=10))


start = DummyOperator(task_id='run_this_first', dag=dag)


streaming = KubernetesPodOperator(
    namespace='airflow',
    image="dpinedaj/spark-python-base:1.0",
    cmds=["python"],
    arguments=["/opt/code/etl/main.py"],
    labels={"foo": "bar"},
    image_pull_policy="Always",
    name="streaming",
    task_id="streaming-task",
    is_delete_operator_pod=False,
    get_logs=True,
    dag=dag
)

batch = KubernetesPodOperator(
    namespace='airflow',
    image="dpinedaj/spark-python-base:1.0",
    cmds=["python", "-c"],
    arguments=["from etl.main import iris_sample;print(iris_sample())"],
    labels={"foo": "bar"},
    image_pull_policy="Always",
    name="batch",
    task_id="batch-task",
    is_delete_operator_pod=False,
    get_logs=True,
    dag=dag
)

streaming.set_upstream(start)
batch.set_upstream(start)