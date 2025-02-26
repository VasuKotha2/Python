import paramiko
import time

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

linux = {'hostname': '192.168.0.50', 'port': '22', 'username':'u1', 'password': 'pass123'}
print(f'Connecting to {linux["hostname"]}')
ssh_client.connect(**linux, look_for_keys=False, allow_agent=False)

stdin, stdout, stderr = ssh_client.exec_command('sudo useradd u2\n', get_pty=True)

stdin.write('pass123\n')  # this is the sudo password
time.sleep(2)  #waiting for the remote server to finish

stdin, stdout, stderr = ssh_client.exec_command('cat /etc/passwd\n')
print(stdout.read().decode())
time.sleep(1)


if ssh_client.get_transport().is_active() == True:
    print('Closing connection')
    ssh_client.close()