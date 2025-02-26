import paramiko
import time

# creating an ssh client object
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

router = {'hostname': '10.1.1.10', 'port': '22', 'username':'u1', 'password':'cisco', 'look_for_keys': False, 'allow_agent': False}
print(f'Connecting to {router["hostname"]}')
ssh_client.connect(**router)


shell = ssh_client.invoke_shell()
shell.send('show users\n')
time.sleep(1)

output = shell.recv(100000).decode()
print(output)


if ssh_client.get_transport().is_active():
    print('Closing connection')
    ssh_client.close()
