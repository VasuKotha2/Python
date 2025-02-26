from netmiko import ConnectHandler

cisco_device = {
    'device_type': 'cisco_ios',
    'host': '10.1.1.10',
    'username': 'u1',
    'password': 'cisco',
    'port': 22,
    'secret': 'cisco',
    'verbose': True
}

connection = ConnectHandler(**cisco_device)

print('Entering the enable mode ...')
connection.enable()

# executing commands
output1 = connection.send_command('show ip int brief')
output2 = connection.send_command('show run')

# getting the prompt
prompt = connection.find_prompt()
# print(prompt)

# remove last char of the prompt (getting the hostname)
hostname = prompt[:-1]

# constructing the file names
filename1 = f'{hostname}-interfaces.txt'
filename2 = f'{hostname}-running-config.txt'

# saving the outputs to files
with open(filename1, 'w') as f:
    f.write(output1)

with open(filename2, 'w') as f:
    f.write(output2)

print(f'Disconnecting from {cisco_device["host"]}')
connection.disconnect()