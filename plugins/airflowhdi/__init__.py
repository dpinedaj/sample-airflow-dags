from airflow.plugins_manager import AirflowPlugin

from .hooks import AzureHDInsightHook
from .operators import (
    AzureHDInsightCreateClusterOperator, 
    ConnectedAzureHDInsightCreateClusterOperator, 
    AzureHDInsightDeleteClusterOperator)
from .sensors import (
    AzureHDInsightClusterSensor,
    AzureDataLakeStorageGen1WebHdfsSensor,
    WasbWildcardPrefixSensor)

class HDInsightPlugin(AirflowPlugin):
    name = 'hd_insight_plugin'
    operators = [AzureHDInsightCreateClusterOperator,
                 ConnectedAzureHDInsightCreateClusterOperator,
                 AzureHDInsightDeleteClusterOperator]
    sensors = [AzureHDInsightClusterSensor,
               AzureDataLakeStorageGen1WebHdfsSensor,
               WasbWildcardPrefixSensor]
    hooks = [AzureHDInsightHook]
