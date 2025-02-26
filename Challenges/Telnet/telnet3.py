import telnetlib
import time

# connecting to the remote device (telnet server)
tn = telnetlib.Telnet('10.1.1.10')

tn.read_until(b'Username: ')
tn.write(b'u1\n')  # sending the username

tn.read_until(b'Password: ')
tn.write(b'cisco\n')  # sending the user's password

tn.write('enable\n'.encode())
tn.write('cisco\n'.encode())

tn.write('terminal length 0\n'.encode())
tn.write('show run\n'.encode())
## the same with:
# tn.write(b'show run\n')
tn.write(b'exit\n')
time.sleep(1)

# getting and printing the output
output = tn.read_all()
output = output.decode()
# print(output)
with open('running-config.txt', 'w') as f:
    f.write(output)