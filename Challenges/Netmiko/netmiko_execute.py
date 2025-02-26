from netmiko import ConnectHandler

def execute(device, command):
    connection = ConnectHandler(**device)
    output = connection.send_command(command)
    print(output)
    connection.disconnect()


cisco_device = {
    'device_type': 'cisco_ios',
    'host': '10.1.1.10',
    'username': 'u1',
    'password': 'cisco',
    'port': 22,
    'secret': 'cisco',
    'verbose': True
}
execute(cisco_device, 'show version')

linux = {
    'device_type': 'linux',
    'host': '192.168.0.50',
    'username': 'u1',
    'password': 'pass123',
    'port': 22,
    'secret': 'pass123',
    'verbose': True
}
execute(linux, 'ifconfig')


