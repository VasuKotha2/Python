import telnetlib
import time

# connecting to the remote device (telnet server)
tn = telnetlib.Telnet('10.1.1.10')

tn.read_until(b'Username: ')
tn.write(b'u1\n')  # sending the username

tn.read_until(b'Password: ')
tn.write(b'cisco\n')  # sending the user's password

# https://drive.google.com/open?id=1Ct_t5TDeR47qYi4E38YSHPmB5z15qoKS
with open('commands.txt', 'r') as f:
    commands = f.read().splitlines()
    print(commands)

for cmd in commands:
    print(f'Executing {cmd}')
    tn.write(cmd.encode() + b'\n')
    time.sleep(1)


tn.write(b'exit\n')
time.sleep(2)

# getting and printing the output
output = tn.read_all().decode()
print(output)
