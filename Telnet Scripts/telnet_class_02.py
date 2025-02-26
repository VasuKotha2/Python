import time

class Device:
    def __init__(self, host, username, password, tn=None):
        self.host = host
        self.username = username
        self.password = password
        self.tn = tn

    def connect(self):
        import telnetlib
        self.tn = telnetlib.Telnet(self.host)

    def authenticate(self):
        self.tn.read_until(b'Username: ')
        self.tn.write(self.username.encode() + b'\n')

        self.tn.read_until(b'Password: ')
        self.tn.write(self.password.encode() + b'\n')

    def send(self, command, timeout=0.5):
        print(f'Sending command: {command}')
        self.tn.write(command.encode() + b'\n')
        time.sleep(timeout)

    def show(self):
        output = self.tn.read_all().decode('utf-8')
        return output


# defining a dict for each router
r1_dict = {'host': '10.1.1.10', 'username': 'u1', 'password': 'cisco', 'enable_password': 'cisco', 'loopback_ip': '1.1.1.1'}
r2_dict = {'host': '10.1.1.20', 'username': 'u1', 'password': 'cisco', 'enable_password': 'cisco', 'loopback_ip': '2.2.2.2'}
r3_dict = {'host': '10.1.1.30', 'username': 'u1', 'password': 'cisco', 'enable_password': 'cisco', 'loopback_ip': '3.3.3.3'}


# list of dictionaries
routers = [r1_dict, r2_dict, r3_dict]

# interating over the list (routers in the topology)
for r in routers:
    router = Device(host=r['host'], username=r['username'], password=r['password'])
    router.connect()
    router.authenticate()
    router.send('enable')
    router.send(r['enable_password'])
    router.send('conf t')
    router.send('int loopback 0')
    router.send(f'ip address {r["loopback_ip"]} 255.255.255.255')
    router.send('exit')
    router.send('router ospf 1')
    router.send('net 0.0.0.0 0.0.0.0 area 0')
    router.send('end')
    router.send('terminal length 0')
    router.send('show ip protocols')
    router.send('exit')
    output = router.show()
    print(output)
    print('#' * 50)
