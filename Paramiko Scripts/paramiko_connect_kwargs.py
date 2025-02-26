import paramiko

# creating an ssh client object
ssh_client = paramiko.SSHClient()
# print(type(ssh_client))

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh_client.connect(hostname='10.1.1.10', port='22', username='u1', password='cisco',
#                    look_for_keys=False, allow_agent=False)

router = {'hostname': '10.1.1.10', 'port': '22', 'username':'u1', 'password':'cisco'}
print(f'Connecting to {router["hostname"]}')
ssh_client.connect(**router, look_for_keys=False, allow_agent=False)  # using **kwargs

# checking if the connection is active
print(ssh_client.get_transport().is_active())

# sending commands
# ...

print('Closing connection')
ssh_client.close()