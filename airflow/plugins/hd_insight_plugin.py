from airflow.plugins_manager import AirflowPlugin

from operators import (HDInsightRunCmdOperator, HDInsightCreateClusterOperator,
                       HDInsightDeleteClusterOperator)
from hooks import HDInsightHook


class HDInsightPlugin(AirflowPlugin):
    name = 'hd_insight_plugin'
    operators = [HDInsightRunCmdOperator,
                 HDInsightCreateClusterOperator, HDInsightDeleteClusterOperator]
    hooks = [HDInsightHook]
