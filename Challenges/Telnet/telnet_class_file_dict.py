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

    def send_form_list(self, commands):
        for cmd in commands:
            self.send(cmd)

    # new method that sends all the commands from a file
    def send_from_file(self, file):
        with open(file, 'r') as f:
            commands = f.read().splitlines()
            # print(commands)
            for cmd in commands:
                self.send(cmd)

    def show(self):
        output = self.tn.read_all().decode('utf-8')
        return output


r1 = {'host': '10.1.1.10', 'username': 'u1', 'password': 'cisco', 'config':'ospf.txt'}
r2 = {'host': '10.1.1.20', 'username': 'u1', 'password': 'cisco', 'config':'eigrp.txt'}
r3 = {'host': '10.1.1.30', 'username': 'u1', 'password': 'cisco', 'config':'router3.conf'}

routers = [r1, r2, r3]
for r in routers:
    router = Device(host=r['host'], username=r['username'], password=r['password'])
    router.connect()
    router.authenticate()

    router.send_from_file(r['config'])
    output = router.show()
    print(output)
    print('#' * 50)