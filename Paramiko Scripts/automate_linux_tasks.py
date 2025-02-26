import myparamiko  # myparamiko.py should be in the same directory with this script (or in sys.path)

# connecting the the Linux VM
client = myparamiko.connect('192.168.0.50', '22', 'u1', 'pass123')
shell = myparamiko.get_shell(client)

# start executing commands
myparamiko.send_command(shell, 'uname -a')

cmd = 'sudo groupadd developers'
myparamiko.send_command(shell, cmd)
myparamiko.send_command(shell, 'pass123', 2)  # pass123 is the sudo password

# myparamiko.show(shell)
myparamiko.send_command(shell, 'tail -n 1 /etc/group')

output = myparamiko.show(shell)
print(output)


# closing the connection
myparamiko.close(client)