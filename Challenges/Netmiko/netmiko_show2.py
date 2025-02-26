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
print(output1)
print('#' * 50)
output2 = connection.send_command('show run')
print(output2)

print(f'Disconnecting from {cisco_device["host"]}')
connection.disconnect()