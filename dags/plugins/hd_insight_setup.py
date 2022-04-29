
from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
from utils.connections import ssh_sftp_conn

server = "test-hdinsight-ssh.azurehdinsight.net"
username = "sshuser"
password = "TestPassword123+"





class HdInsightSetupOperator(BaseOperator):
    def __init__(self, host, username, password, *args, **kwargs):
        super(HdInsightSetupOperator, self).__init__(*args, **kwargs)
        self._host = host
        self._username = username
        self._password = password

    def execute(self, context):
        self._setup_ssh()

    def _setup_ssh(self):
        with ssh_sftp_conn(self._host, self._username, self._password) as (ssh_client, sftp_client):
            sftp_client.put('setup_hdi.sh', 'setup_hdi.sh')
            ssh_client.exec_command(
                'mv setup_hdi.sh /home/{}/'.format(self._username))
            ssh_client.exec_command(
                'chmod 777 /home/{}/setup_hdi.sh'.format(self._username))
            ssh_client.exec_command(
                'sh /home/{}/setup_hdi.sh'.format(self._username))
            ssh_client.exec_command(
                'rm /home/{}/setup_hdi.sh'.format(self._username))


class HdInsightSetupPlugin(AirflowPlugin):
    name = 'hd_insight_setup_plugin'
    operators = [HdInsightSetupOperator]