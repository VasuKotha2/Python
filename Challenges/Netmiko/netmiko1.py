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

print('Entering the global configuration mode ...')
connection.config_mode()

# executing commands
print('Creating a user ...')
connection.send_command('username admin secret topsecret')

connection.exit_config_mode()

print('Saving the configuration ...')
connection.send_command('write')


print(f'Disconnecting from {cisco_device["host"]}')
connection.disconnect()