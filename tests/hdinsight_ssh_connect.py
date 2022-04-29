import paramiko
server = "test-hdinsight-ssh.azurehdinsight.net"
username = "sshuser"
password = "---"
cmd_to_execute = "echo 'test_from_python' > test_from_python.txt"
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server, username=username, password=password)
stdin, stdout, stderr = client.exec_command(cmd_to_execute)
stdin.close()