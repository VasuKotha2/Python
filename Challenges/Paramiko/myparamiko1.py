import paramiko
import time

def connect(server_ip, server_port, user, passwd):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'Connecting to {server_ip}')
    ssh_client.connect(hostname=server_ip, port=server_port, username=user, password=passwd,
                       look_for_keys=False, allow_agent=False)
    return ssh_client

def get_shell(ssh_client):
    shell = ssh_client.invoke_shell()
    return shell

def send_command(shell, command, timout=1):
    print(f'Sending command: {command}')
    shell.send(command + '\n')
    time.sleep(timout)


### SOLUTION ###
def send_from_list(shell, commands):
   for cmd in commands:
      send_command(shell, cmd)


def show(shell, n=10000):
    output = shell.recv(n)
    return output.decode()

def close(ssh_client):
    if ssh_client.get_transport().is_active() == True:
        print('Closing connection')
        ssh_client.close()

if __name__ == '__main__':
    router1 = {'server_ip': '10.1.1.10', 'server_port': '22', 'user':'u1', 'passwd':'cisco'}
    client = connect(**router1)
    shell = get_shell(client)

    # the second element (cisco) is the enable command
    commands = ['enable', 'cisco', 'conf t', 'username admin1 secret cisco', 'access-list 1 permit any', 'end',
                'terminal length 0', 'sh run | i user']
    
    send_from_list(shell, commands)

    output = show(shell)
    print(output)



