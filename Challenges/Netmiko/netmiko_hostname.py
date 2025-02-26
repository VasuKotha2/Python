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

# getting the prompt
prompt = connection.find_prompt()
# print(prompt)

# remove last char of the prompt (getting the hostname)
hostname = prompt[:-1]

print(f'Hostname: {hostname}')

print(f'Disconnecting from {cisco_device["host"]}')
connection.disconnect()