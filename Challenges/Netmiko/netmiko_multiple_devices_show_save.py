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

    # getting the prompt
    prompt = connection.find_prompt()
    # print(prompt)

    # remove the last char from the prompt (getting the hostname)
    hostname = prompt[:-1]

    # getting the current date
    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day

    filename = f'{hostname}_{year}-{month}-{day}.txt'
    with open(filename, 'w') as f:
        print(f'Saving output to: {filename}')
        f.write(output)


    # print(output)
    # print(f'Disconnecting from {cisco_device["host"]}')
    connection.disconnect()
    print('#' * 50)