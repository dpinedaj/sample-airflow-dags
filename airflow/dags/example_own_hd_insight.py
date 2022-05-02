
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.hd_insight_plugin import HDInsightRunCmdOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(seconds=30),
    'max_active_runs': 1
}


dag = DAG(
    'hd_insight_setup_dag',
    default_args=default_args,
    description='submit sh file to hd_insights',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
)

t1 = HDInsightRunCmdOperator(
    task_id='hd_insight_setup',
    host="test-hdinsight-ssh.azurehdinsight.net",
    username="sshuser",
    cmd="setup_hdi.sh",
    password="TestPassword123+",
    do_xcom_push=True,
    dag=dag,
)

t1