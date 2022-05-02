from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from hooks.hdinsight_hook import HDInsightHook


class HDInsightDeleteClusterOperator(BaseOperator):
    """
    :param azure_conn_id: connection id of a service principal
        which will be used to delete Hdinsight cluster
    :type azure_conn_id: str
    :param cluster_name: cluster name of will  deleting
    :type cluster_name: str
    """

    @apply_defaults
    def __init__(self,
                 cluster_name,
                 azure_conn_id='azure_hdinsight_default',
                 *args,
                 **kwargs
                 ):
        super(HDInsightDeleteClusterOperator, self).__init__(*args, **kwargs)
        self.cluster_name = cluster_name
        self.azure_conn_id = azure_conn_id

    def execute(self, context):
        azure_hook = HDInsightHook(azure_conn_id=self.azure_conn_id)
        self.log.info("Executing HDInsightDeleteClusterOperator ")
        azure_hook.delete_cluster(cluster_name=self.cluster_name)
        self.log.info("Finished executing HDInsightDeleteClusterOperator")
