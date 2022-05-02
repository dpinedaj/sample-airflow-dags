
import paramiko
from contextlib import contextmanager

@contextmanager
def ssh_sftp_conn(host, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, username=username, password=password)
    sftp_client = ssh_client.open_sftp()
    yield ssh_client, sftp_client
    ssh_client.close()
    sftp_client.close()