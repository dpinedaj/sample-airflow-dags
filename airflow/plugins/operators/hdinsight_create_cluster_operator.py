from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from azure.mgmt.hdinsight.models import ClusterCreateProperties

from hooks.hdinsight_hook import HDInsightHook


class HDInsightCreateClusterOperator(BaseOperator):
    """
    See https://docs.microsoft.com/en-us/python/api/overview/azure/hdinsight?view=azure-python

    :param azure_conn_id: connection id of a service principal
            which will be used to delete Hdinsight cluster
    :type azure_conn_id: str
    :param cluster_name: cluster name of will  creating
    :type cluster_name: str
    """

    @apply_defaults
    def __init__(self,
                 cluster_name,
                 cluster_params: ClusterCreateProperties,
                 azure_conn_id='azure_hdinsight_default',
                 *args,
                 **kwargs
                 ):
        super(HDInsightCreateClusterOperator, self).__init__(*args, **kwargs)

        self.cluster_name = cluster_name
        self.cluster_params = cluster_params
        self.azure_conn_id = azure_conn_id

    def execute(self, context):
        azure_hook = HDInsightHook(azure_conn_id=self.azure_conn_id)
        self.log.info("Executing HDInsightCreateClusterOperator ")
        azure_hook.create_cluster(self.cluster_params, self.cluster_name)
        self.log.info("Finished executing HDInsightCreateClusterOperator")
