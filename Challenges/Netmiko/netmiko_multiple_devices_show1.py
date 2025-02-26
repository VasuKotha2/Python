from netmiko import ConnectHandler

devices = ['10.1.1.10', '192.168.122.20', '192.168.122.30']

for dev in devices:
    cisco_device = {
        'device_type': 'cisco_ios',
        'host': dev,
        'username': 'u1',
        'password': 'cisco',
        'port': 22,
        'secret': 'cisco',
        'verbose': True
    }

    connection = ConnectHandler(**cisco_device)

    output = connection.send_command('show ip int brief')
    print(output)
    # print(f'Disconnecting from {cisco_device["host"]}')
    connection.disconnect()
    print('#' * 50)