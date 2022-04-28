from datetime import datetime, timedelta
from airflow import DAG

from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor




dag = DAG(
    'spark_pi',
    default_args={'max_active_runs': 1},
    description='submit spark-pi as sparkApplication on kubernetes',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
)

t1 = SparkKubernetesOperator(
    task_id='spark_pi_submit',
    namespace="airflow",
    application_file=open("/opt/airflow/dags/repo/dags/example_spark_kubernetes_spark_pi.yaml").read(),
    do_xcom_push=True,
    dag=dag,
)

t2 = SparkKubernetesSensor(
    task_id='spark_pi_monitor',
    namespace="airflow",
    application_name="{{ task_instance.xcom_pull(task_ids='spark_pi_submit')['metadata']['name'] }}",
    dag=dag,
)
t1 >> t2