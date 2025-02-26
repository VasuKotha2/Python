import paramiko
import time
import getpass
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# prompting for the user's password securely
password = getpass.getpass('Enter password:')

router = {'hostname': '10.1.1.10', 'port': '22', 'username':'u1', 'password': password}
print(f'Connecting to {router["hostname"]}')
ssh_client.connect(**router, look_for_keys=False, allow_agent=False)

shell = ssh_client.invoke_shell()
shell.send('terminal length 0\n')
shell.send('show version\n')
shell.send('show ip int brief\n')
time.sleep(1)

output = shell.recv(10000)
# print(type(output))
output = output.decode('utf-8')
print(output)


if ssh_client.get_transport().is_active() == True:
    print('Closing connection')
    ssh_client.close()