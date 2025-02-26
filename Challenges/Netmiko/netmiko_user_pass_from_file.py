from netmiko import ConnectHandler

with open('credentials.txt') as f:
    content_list = f.read().split(':')
    # print(content_list) # ['10.1.1.10', '22', 'u1', 'cisco', 'cisco']

cisco_device = {
    'device_type': 'cisco_ios',
    'host': content_list[0],
    'username': content_list[2],
    'password': content_list[3],
    'port': content_list[1],
    'secret': content_list[4],
    'verbose': True
}

connection = ConnectHandler(**cisco_device)
output = connection.send_command('show arp')
print(output)


print(f'Disconnecting from {cisco_device["host"]}')
connection.disconnect()