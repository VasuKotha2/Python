import telnetlib
import time

host = '10.1.1.10'
port = '23'
user = 'u1'
password = 'cisco'

tn = telnetlib.Telnet(host=host, port=port)

tn.read_until(b'Username: ')
tn.write(user.encode() + b'\n')

tn.read_until(b'Password: ')
tn.write(password.encode() + b'\n')

tn.write(b'terminal length 0\n')
# tn.write(b'show ip interface brief\n')
tn.write('show ip int brief\n'.encode())
tn.write(b'enable\n')
tn.write(b'cisco\n') # this is the enable password
tn.write(b'show run\n')
tn.write(b'exit\n')
time.sleep(1)

output = tn.read_all()
print(type(output))
output = output.decode()
print(output)