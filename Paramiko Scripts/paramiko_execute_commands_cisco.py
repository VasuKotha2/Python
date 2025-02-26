import paramiko
import time

# creating an ssh client object
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

router = {'hostname': '10.1.1.10', 'port': '22', 'username':'u1', 'password':'cisco'}
print(f'Connecting to {router["hostname"]}')
ssh_client.connect(**router, look_for_keys=False, allow_agent=False)

# creating a shell object
shell = ssh_client.invoke_shell()

# sending commads to the remote device to execute them
# each command ends  in \n (new line, the enter key)
shell.send('terminal length 0\n')
shell.send('show version\n')
shell.send('show ip int brief\n')
time.sleep(1)  # waiting for the remove device to finish executing the commands (mandatory)

# reading from the shell's output buffer
output = shell.recv(10000)
# print(type(output))
output = output.decode('utf-8')  # decoding from bytes to string
print(output)

# closing the connection if it's active
if ssh_client.get_transport().is_active() == True:
    print('Closing connection')
    ssh_client.close()