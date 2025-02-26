import paramiko
import time

# creating an ssh client object
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print('Connecting to 10.1.1.10')
ssh_client.connect(hostname='10.1.1.10', port='22', username='u1', password='cisco',
                   look_for_keys=False, allow_agent=False)


shell = ssh_client.invoke_shell()

# the second element (cisco) is the enable command
commands = ['enable', 'cisco', 'conf t', 'username admin1 secret cisco', 'access-list 1 permit any', 'end',
            'terminal length 0',  'sh run | i user']


for cmd in commands:
    print(f'Sending command: {cmd}')
    shell.send(f'{cmd}\n')
    time.sleep(0.5)

output = shell.recv(100000)
# decoding from bytes to string
output = output.decode()
print(output)


if ssh_client.get_transport().is_active():
    print('Closing connection')
    ssh_client.close()
