
from airflow.models import BaseOperator
from utils.connections import ssh_sftp_conn



class HdInsightRunCmdOperator(BaseOperator):
    def __init__(self, host, username, password, cmd, *args, **kwargs):
        super(HdInsightRunCmdOperator, self).__init__(*args, **kwargs)
        self._host = host
        self._username = username
        self._password = password
        self._cmd = cmd

    def execute(self, context):
        self._setup_ssh()

    def _setup_ssh(self):
        with ssh_sftp_conn(self._host, self._username, self._password) as (ssh_client, sftp_client):
            # TODO: Reemplazar setuo_hdi por el cmd y validar si es string o file, y si requiere sft o no.
            sftp_client.put('setup_hdi.sh', 'setup_hdi.sh')
            ssh_client.exec_command(
                'mv setup_hdi.sh /home/{}/'.format(self._username))
            ssh_client.exec_command(
                'chmod 777 /home/{}/setup_hdi.sh'.format(self._username))
            ssh_client.exec_command(
                'sh /home/{}/setup_hdi.sh'.format(self._username))
            ssh_client.exec_command(
                'rm /home/{}/setup_hdi.sh'.format(self._username))


