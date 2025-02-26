import paramiko
import time
import threading

def execute_command(device, command):

    # creating an ssh client object
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    print(f'Connecting to {device["hostname"]}')
    ssh_client.connect(**device)


    shell = ssh_client.invoke_shell()
    print(f'\nSending command "{command}" to "{device["hostname"]}"')
    shell.send('term length 0\n')
    shell.send(f'{command}\n')
    time.sleep(1)

    output = shell.recv(100000).decode()
    print(output)


    if ssh_client.get_transport().is_active():
        print('Closing connection')
        ssh_client.close()


if __name__ == '__main__':
    router1 = {'hostname': '10.1.1.10', 'port': '22', 'username': 'u1', 'password': 'cisco',
                  'look_for_keys': False, 'allow_agent': False}
    router2 = {'hostname': '10.1.1.20', 'port': '22', 'username': 'u1', 'password': 'cisco',
                  'look_for_keys': False, 'allow_agent': False}
    router3 = {'hostname': '10.1.1.30', 'port': '22', 'username': 'u1', 'password': 'cisco',
                  'look_for_keys': False, 'allow_agent': False}

    routers = [router1, router2, router3]

    for device in routers:
        execute_command(device, 'show ip interface brief')
