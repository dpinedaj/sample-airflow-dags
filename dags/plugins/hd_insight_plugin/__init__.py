from airflow.plugins_manager import AirflowPlugin

from .operators import HdInsightRunCmdOperator, HdInsightCreateClusterOperator, HdInsightDeleteClusterOperator
from .hooks import AzureHDInsightHook

class HdInsightPlugin(AirflowPlugin):
    name = 'hd_insight_plugin'
    operators = [HdInsightRunCmdOperator, HdInsightCreateClusterOperator, HdInsightDeleteClusterOperator]
    hooks = [AzureHDInsightHook]