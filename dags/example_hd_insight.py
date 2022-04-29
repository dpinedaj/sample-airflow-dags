"""
Create azure_default connection  for cluster creating
Exanmple:
Firstly
    Set an environment variable for AZURE_AUTH_LOCATION:
    export AZURE_AUTH_LOCATION=~/.azure/azure_credentials.json
References:
    docs.microsoft.com/en-us/python/azure/python-sdk-azure-authenticate?view=azure-python
Conn Id: azure_default
Conn Type : None
Host   : None
Schema : None
Login  : azure client_id
Password  : azure client_secret
Port   : None
Extra : {
  "key_path": "~/.azure/azure_credentials.json",
  "subscriptionId": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
  "tenantId": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
  "resource_group_name": "example_rg",
  "resource_group_location": "example_rg_location"
}
References:
    docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal
After Create Hortonworks Ambari connection  for submitting jobs
Conn Id: hortonworks_ambari_default
Conn Type : None
Host   : https://cluster_name.azurehdinsight.net
Schema : https
Login  : Cluster user name
Password  : cluster password
Port   : None (or Optional)
"""
from airflowhdi.sensors.azure_hdinsight_cluster_sensor import AzureHDInsightClusterSensor
from airflowlivy.sensors.livy_batch_sensor import LivyBatchSensor
from airflowlivy.operators.livy_batch_operator import LivyBatchOperator
from airflowhdi.operators.azure_hdinsight_delete_cluster_operator \
    import AzureHDInsightDeleteClusterOperator
from airflowhdi.operators.azure_hdinsight_create_cluster_operator \
    import ConnectedAzureHDInsightCreateClusterOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils import dates
from airflow import DAG, AirflowException
from datetime import timedelta
from airflow.operators.python_operator import PythonOperator
from azure.mgmt.hdinsight.models import ClusterCreateProperties, \
    OSType, Tier, ClusterDefinition, ComputeProfile, Role, \
    HardwareProfile, LinuxOperatingSystemProfile, OsProfile, \
    StorageProfile, StorageAccount

cluster_params: ClusterCreateProperties = ClusterCreateProperties(
    cluster_version="3.6",
    os_type=OSType.linux,
    tier=Tier.standard,
    cluster_definition=ClusterDefinition(
        kind="spark",
        configurations={
            "gateway": {
                "restAuthCredential.enabled_credential": "True",
                "restAuthCredential.username": "username",
                "restAuthCredential.password": "password"
            }
        }
    ),
    compute_profile=ComputeProfile(
        roles=[
            Role(
                name="headnode",
                target_instance_count=2,
                hardware_profile=HardwareProfile(vm_size="Large"),
                os_profile=OsProfile(
                    linux_operating_system_profile=LinuxOperatingSystemProfile(
                        username="username",
                        password="password"
                    )
                )
            ),
            Role(
                name="workernode",
                target_instance_count=1,
                hardware_profile=HardwareProfile(vm_size="Large"),
                os_profile=OsProfile(
                    linux_operating_system_profile=LinuxOperatingSystemProfile(
                        username="username",
                        password="password"
                    )
                )
            )
        ]
    ),
    storage_profile=StorageProfile(
        storageaccounts=[StorageAccount(
            name="storage_account",
            key="storage_account_key",
            container="container",
            is_default=True
        )]
    )
)


default_args = {
    'owner': 'angad',
    'depends_on_past': False,
    'start_date': dates.days_ago(1),
    "retries": 0
}

cluster_name = "airflowtesthdi"

AZURE_CONN_ID = 'azure_hdi_default'
HDI_CONN_ID = 'azure_hdi_cluster_params_default'


def handle_failure_task():
    raise AirflowException('Marking DAG as failed due to an upstream failure!')


with DAG(dag_id='example_azure_hdinsight_dag',
         default_args=default_args,
         dagrun_timeout=timedelta(hours=2),
         max_active_runs=1,
         schedule_interval=None,
         catchup=False,
         doc_md=__doc__) as dag:

    create_cluster_op = ConnectedAzureHDInsightCreateClusterOperator(task_id="start_cluster",
                                                                     azure_conn_id=AZURE_CONN_ID,
                                                                     hdi_conn_id=HDI_CONN_ID,
                                                                     cluster_name=cluster_name,
                                                                     cluster_params=cluster_params,
                                                                     trigger_rule=TriggerRule.ALL_SUCCESS)

    monitor_cluster_provisioning_op = AzureHDInsightClusterSensor(cluster_name,
                                                                  azure_conn_id=AZURE_CONN_ID,
                                                                  task_id='hdi_provisioning_sensor',
                                                                  poke_interval=5,
                                                                  provisioning_only=True)

    # TODO: SSHOPerator para preparar el cluster, clonar el codigo y descargar jars en spark_home/jars

    monitor_cluster_op = AzureHDInsightClusterSensor(cluster_name,
                                                     azure_conn_id=AZURE_CONN_ID,
                                                     task_id='hdi_cluster_sensor',
                                                     poke_interval=5)

    handle_failure_op = PythonOperator(
        task_id='handle_failure',
        python_callable=handle_failure_task,
        trigger_rule=TriggerRule.ONE_FAILED)

    livy_submit = LivyBatchOperator(
        task_id='livy_submit',
        name="batch_example_{{ run_id }}",
        # file='wasb:///example/jars/spark-examples.jar',
        file="file:///opt/code/etl/main.py",
        py_files=["file:///opt/code/etl/main.py"]
        arguments=[10],
        num_executors=1,
        azure_conn_id=AZURE_CONN_ID,
        cluster_name=cluster_name,
        conf={
            'spark.shuffle.compress': 'false',
        },
        class_name='org.apache.spark.examples.SparkPi',
        proxy_user='admin',
        trigger_rule=TriggerRule.ALL_SUCCESS,
        execution_timeout=timedelta(minutes=10)
    )

    livy_sensor = LivyBatchSensor(
        batch_id="{{ task_instance.xcom_pull('livy_submit', key='return_value') }}",
        task_id='livy_sensor',
        azure_conn_id=AZURE_CONN_ID,
        cluster_name=cluster_name,
        verify_in="yarn",
        poke_interval=20,
        timeout=600,
    )

    terminate_cluster_op = AzureHDInsightDeleteClusterOperator(task_id="delete_cluster",
                                                               azure_conn_id=AZURE_CONN_ID,
                                                               cluster_name=cluster_name,
                                                               trigger_rule=TriggerRule.ALL_DONE)

    create_cluster_op >> monitor_cluster_provisioning_op >> monitor_cluster_op >> handle_failure_op
    monitor_cluster_provisioning_op >> livy_submit >> livy_sensor >> terminate_cluster_op

if __name__ == '__main__':
    dag.clear(reset_dag_runs=True)
    dag.run()
