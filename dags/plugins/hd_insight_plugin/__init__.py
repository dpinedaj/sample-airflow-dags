from airflow.plugins_manager import AirflowPlugin

from .operators import HDInsightRunCmdOperator, HDInsightCreateClusterOperator, HDInsightDeleteClusterOperator
from .hooks import AzureHDInsightHook

class HdInsightPlugin(AirflowPlugin):
    name = 'hd_insight_plugin'
    operators = [HDInsightRunCmdOperator, HDInsightCreateClusterOperator, HDInsightDeleteClusterOperator]
    hooks = [AzureHDInsightHook]