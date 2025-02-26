import concurrent.futures
import re
import time
import socket
import subprocess
import os
try:
    import pexpect
except ModuleNotFoundError:
    pass
import threading
import json
import sys
from concurrent.futures import ThreadPoolExecutor


device_results = {}

def check_snmp_status(snmp_read, device_ip):
    response_2 = os.system("snmpwalk -v2c -c " + snmp_read + " " + device_ip + " 1.3.6.1.2.1.1.1")
    snmp_value = str(response_2).rsplit("\n",1)[-1]
    if int(snmp_value) == 0:
        return "Reachable"
    else:
        if device_ip == "175.175.173.40":
            return " "
        else:
            return "Unreachable"

def check_ping_for_servers(device_details):
    device_ip = device_details['DEVICE_IP']
    ping_status = check_ping_status(device_ip)
    if ping_status == "Reachable":
        ping_font = " "
    else:
        ping_font = "FF0000"
    device_details['telnet_status'] = " "
    device_details['telnet_font'] = " "
    device_details['ping_status'] = ping_status
    device_details['snmp_status'] = " "
    device_details['snmp_font'] = " "

    print("Ping is done for server ip - ", device_ip)
    return device_details

def check_ping_status(device_ip):
    response = os.system("ping -c 1 " + device_ip)
    if response == 0:
        return "Reachable"
    else:
        return "Unreachable"
    
def check_telnet_login(host, username, password, enable_password, real_or_virtual, device_type):
    time.sleep(3)
    show_clock_output = ""
    print("Checking Telnet status for device - ", host)
    child = pexpect.spawn("telnet {}".format(host))
    index = child.expect(["Us", "User", "login", "testlogin", ".*?>", ".*?#"])
    if index == 2 or index == 3: #If in case direct login
        output = "Auth Success - Direct Login"
        child.close()
    else:
        child.sendline(username)
        child.expect(["Pa", "Password", "testpass"], timeout=10)
        child.sendline(password)
        time.sleep(3)
        output = str(child.read_nonblocking(size = 1000, timeout=10))
        print("first output = ", output)
        if "failed" in output.lower() or "password" in output.lower():
            print("Inside")
            output = "Authentication Failed or it is asking for password again - {} ".format(output)
            child.close()
            return output, show_clock_output
        else:
            child.sendline("enable")
            time.sleep(3)
            output = str(child.read_nonblocking(size = 1000, timeout = 10))
            print("first output = ", output)
            if "Password"  in output:
                print("Tring to enter enable password")
                # Asking for password after entering enable mode
                child.sendline(enable_password)
                time.sleep(3)
                output = str(child.read_nonblocking(size = 1000, timeout= 10))
            if "sapro" in real_or_virtual.lower() or "wlc" in device_type.lower():
                show_clock_output = " "
            else:
                child.sendline("show clock")
                time.sleep(4)
                show_clock_output = child.read_nonblocking(size = 1000, timeout= 10).decode("utf-8")
                if "2021" in show_clock_output:
                    show_clock_output = show_clock_output.split("\r\n")[1]
                
            
        child.close()
    print("Completed checking Telnet status for device - ", host)
    return output, show_clock_output

def check_status(device_details):
    """ start and end params indicate the starting row number and ending row number in the excel sheet"""

    show_clock_output = ""
    device_ip = device_details['DEVICE_IP']
    username = device_details['username']
    password = device_details['password']
    enable_password = device_details['enable_password']
    snmp_read = device_details['snmp_read']
    real_or_virtual = device_details['real/virtual']
    device_type = device_details['device_type']
    try:
        telnet_login_check_status = check_telnet_login(device_ip, username, password, enable_password, real_or_virtual, device_type)
        show_clock_output = telnet_login_check_status[1]
        telnet_login_check_status = telnet_login_check_status[0]
    except TimeoutError:
        telnet_login_check_status = "TimeoutError"
    except ConnectionRefusedError:
        telnet_login_check_status = "ConnectionRefusedError"
    except ConnectionResetError:
        telnet_login_check_status = "ConnectionResetError"
    except BrokenPipeError:
        telnet_login_check_status = "BrokenPipeError"
    except socket.timeout:
        telnet_login_check_status = "socket.timeout"
    except Exception as err:
        if "Timeout exceeded" in str(err):
            telnet_login_check_status = "Timeout Exceeded"
        else:
            telnet_login_check_status = str(err)
    if "Authenticeation Failed" in telnet_login_check_status:
        telnet_auth_status = "Auth Failed"
    elif "TimeoutError" in telnet_login_check_status:
        telnet_auth_status = "TimeoutError - Device did not respond"
    elif "ConnectionRefusedError" in telnet_login_check_status:
        telnet_auth_status = "ConnectionRefusedError - Connection refused"
    elif "ConnectionResetError" in telnet_login_check_status:
        telnet_auth_status = "ConnectionResetError"
    elif "BrokenPipeError" in telnet_login_check_status:
        telnet_auth_status = "BrokenPipeError"
    elif "socket.timeout" in telnet_login_check_status:
        telnet_auth_status = "socket.timeout"
    elif "Unkown Error" in telnet_login_check_status:
        telnet_auth_status = telnet_login_check_status
    elif "ConnectionRefused" in telnet_login_check_status:
        telnet_auth_status = "ConnectionRefused"
    elif "User" in telnet_login_check_status:
        telnet_auth_status = "Auth Failed"
    elif "Timeout Exceeded" in telnet_login_check_status:
        telnet_auth_status = "Timeout Exceeded"
    else:
        telnet_auth_status = "Auth Success"

    device_image_response = subprocess.run(
        "snmpwalk -v2c -c " + str(snmp_read) + " " + device_ip + " iso.3.6.1.4.1.9.9.25.1.1.1.2.5", shell=True,
        stdout = subprocess.PIPE).stdout
    regex1 = "\$([a-zA-Z0-9\(\)_\-\.].*)\$"
    regex2 = "Version ([a-zA-Z0-9\.\(\)\:]*)"
    device_image_version = " "
    if re.search(regex1, str(device_image_response)) is not None:
        device_image_version = re.findall(regex1, str(device_image_response))[0]
    else:
        device_image_response = subprocess.run(
            "snmpwalk -v2c -c " + str(snmp_read)
        )


