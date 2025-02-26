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



router = Device('10.1.1.20', 'u1', 'cisco')
router.connect()
router.authenticate()
router.send('enable')
router.send('cisco')
router.send('conf t')
router.send('int loopback 0')
router.send(f'ip address 1.1.1.1 255.255.255.255')
router.send('exit')
router.send('router ospf 1')
router.send('net 0.0.0.0 0.0.0.0 area 0')
router.send('end')
router.send('terminal length 0')
router.send('show ip protocols')
router.send('exit')
output = router.show()
print(output)
