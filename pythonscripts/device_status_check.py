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



# device_data = json.loads(open("device_details.json", "w").read())
device_results = {}
def check_snmp_status(snmp_read,device_ip):
    response_2 = os.system("snmpwalk -v2c -c " + snmp_read + " " + device_ip + " 1.3.6.1.2.1.1.1")
    snmp_value = str(response_2).rsplit("\n", 1)[-1]
    if int(snmp_value) == 0:
        return "Reachable"
    else:
        if device_ip == "175.175.173.40":  # Skipping the ENCS5408 device
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
    device_details['ping_font'] = ping_font
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

def check_telnet_login(host, username, password, enable_password,real_or_virtual,device_type):
    time.sleep(3)
    show_clock_output = ""
    print("Checking Telnet status for device - ",host)
    child = pexpect.spawn("telnet {}".format(host))
    index = child.expect(["Us","User","login","testlogin",".*?>",".*?#"])
    if index == 2 or index == 3: #If in case direct login.
        output = "Auth Success - Direct Login"
        child.close()
    else:
        child.sendline(username)
        # time.sleep(3)
        child.expect(["Pa","Password", "testpass"],timeout=10)
        child.sendline(password)
        time.sleep(3)
        output = str(child.read_nonblocking(size=1000,timeout=10))
        print("first output = ", output)
        if "failed" in output.lower() or "password" in output.lower():
            print("Inside")
            output = "Authentication Failed or it is asking for password again  - {} ".format(output)
            child.close()
            return output,show_clock_output
        else:
            child.sendline("enable")
            time.sleep(3)
            output = str(child.read_nonblocking(size=1000,timeout=10))
            print("first output = ", output)
            if "Password" in output:
                print("Trying to enter enable password")
                # Asking for password after entering enable mode
                child.sendline(enable_password)
                time.sleep(3)
                output = str(child.read_nonblocking(size=1000,timeout=10))
            if "sapro" in real_or_virtual.lower() or "wlc" in device_type.lower():
                show_clock_output = " "
            else:
                child.sendline("show clock")
                time.sleep(4)
                show_clock_output = child.read_nonblocking(size=1000, timeout=10).decode("utf-8")
                if "2021" in show_clock_output:
                    show_clock_output = show_clock_output.split("\r\n")[1]

        child.close()
    print("Completed checking Telnet status for device - ",host)
    return output,show_clock_output



def check_status(device_details):
    """start and end params indicate the starting row number and ending row number in the excel sheet"""
    # print("checking telnet status for device - " + device_ip)
    show_clock_output = ""
    device_ip = device_details['DEVICE_IP']
    username = device_details['username']
    password = device_details['password']
    enable_password = device_details['enable_password']
    snmp_read = device_details['snmp_read']
    real_or_virtual = device_details['real/virtual']
    device_type = device_details['device_type']
    try:
        telnet_login_check_status = check_telnet_login(device_ip, username, password, enable_password, real_or_virtual,
                                                       device_type)
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
    # except pexpect.Exceptions as e:
    #     telnet_login_check_status = "ConnectionRefused"
    except Exception as err:
        if "Timeout exceeded" in str(err):
            telnet_login_check_status = "Timeout Exceeded"
        else:
            telnet_login_check_status = str(err)
    if "Authentication Failed" in telnet_login_check_status:
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
    elif "Unknown Error" in telnet_login_check_status:
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
        stdout=subprocess.PIPE).stdout
    regex1 = "\$([a-zA-Z0-9\(\)_\-\.].*)\$"
    regex2 = "Version ([a-zA-Z0-9\.\(\)\:]*)"
    device_image_version = " "
    if re.search(regex1, str(device_image_response)) is not None:
        device_image_version = re.findall(regex1, str(device_image_response))[0]
    else:
        device_image_response = subprocess.run(
            "snmpwalk -v2c -c " + str(snmp_read) + " " + device_ip + " 1.3.6.1.2.1.1.1", shell=True,
            stdout=subprocess.PIPE).stdout
        if re.search(regex2, str(device_image_response)) is not None:
            device_image_version = re.findall(regex2, str(device_image_response))[0]

    if telnet_auth_status == "Auth Success":
        ping_status = "Reachable"
        ping_font = " "
        telnet_font = " "
    else:
        telnet_font = "FF0000"
        ping_status = check_ping_status(device_ip)
        if ping_status == "Reachable":
            ping_font = " "
        else:
            ping_font = "FF0000"

    snmp_status = check_snmp_status(snmp_read, device_ip)
    if snmp_status == "Reachable" or device_ip == "175.175.173.40":
        snmp_font = " "
    else:
        snmp_font = "FF0000"

    device_details['telnet_status'] = telnet_auth_status
    device_details['telnet_font'] = telnet_font
    device_details['ping_status'] = ping_status
    device_details['ping_font'] = ping_font
    device_details['snmp_status'] = snmp_status
    device_details['snmp_font'] = snmp_font
    device_details['show_clock'] = show_clock_output
    print(device_details)
    print("Everything is done for - ", device_ip)
    return device_details


def change_routes():
    """Change the routes on the device"""
    device_set = sys.argv[1] if len(sys.argv) > 1 else "SET1"
    print("Device Set = ",device_set)
    print("Args = ",sys.argv)
    routes_set2 = ["sudo -S route add -net 175.175.0.0/16 gw 10.197.124.254","sudo -S route add -net 48.0.0.0/8 gw 10.197.124.254","sudo -S route add -net 35.1.1.0/24 gw 10.197.124.254"]
    routes_delete = ["sudo -S route del -net 175.175.0.0/16","sudo -S route del -net 48.0.0.0/8","sudo -S route del -net 35.1.1.0/24"]
    routes_set1 = ["sudo -S route add -net 175.175.0.0/16 gw 175.175.40.1","sudo -S route add -net 48.0.0.0/8 gw 175.175.40.1","sudo -S route add -net 35.1.1.0/24 gw 175.175.40.1"]
    routes_set3 = ["sudo -S route add -net 175.175.0.0/16 gw 175.175.40.2","sudo -S route add -net 48.0.0.0/8 gw 175.175.40.2","sudo -S route add -net 35.1.1.0/24 gw 175.175.40.2"]
    routes_set4 = ["sudo -S route add -net 8.94.20.0/24 gw 175.175.40.1",
                   "sudo -S route add -net 8.94.21.0/24 gw 175.175.40.1",
                   "sudo -S route add -net 175.175.169.0/24 gw 175.175.40.1"]
    routes_set5 = ["sudo -S route add -net 175.175.0.0/16 gw 10.197.124.253","sudo -S route add -net 48.0.0.0/8 gw 10.197.124.253","sudo -S route add -net 35.1.1.0/24 gw 10.197.124.253"]

    for route in routes_delete:
        print(os.system("echo cisco123 | {}".format(route)))
    print("Done deleting existing routes")
    if device_set == "SET1":
        print("Adding routes for set 1 devices")
        for route in routes_set1:
            print(os.system("echo cisco123 | {}".format(route)))
    elif device_set == "SET2":
        print("Adding routes for set 2 devices")
        for route in routes_set2:
            print(os.system("echo cisco123 | {}".format(route)))
    elif device_set == "SET3":
        print("Adding routes for set 3 devices")
        for route in routes_set3:
            print(os.system("echo cisco123 | {}".format(route)))
    elif device_set == "SET4":
        print("Adding routes for set 4 devices")
        for route in routes_set4:
            print(os.system("echo cisco123 | {}".format(route)))
    elif device_set == "SET5":
        print("Adding routes for set 5 devices")
        for route in routes_set5:
            print(os.system("echo cisco123 | {}".format(route)))


def call_threading_process_servers(value):
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit the function for each dictionary and store the Future objects
        futures = [executor.submit(check_ping_for_servers, input_dict) for input_dict in value]

        # Retrieve and process the results as they become available
        for future in concurrent.futures.as_completed(futures):
            modified_dict = future.result()
            # print("Modified dictionary:", modified_dict)
            results.append(modified_dict)
    return results
def call_threading_process(value):
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit the function for each dictionary and store the Future objects
        futures = [executor.submit(check_status, input_dict) for input_dict in value]

        # Retrieve and process the results as they become available
        for future in concurrent.futures.as_completed(futures):
            modified_dict = future.result()
            modified_dict = future.result()
            # print("Modified dictionary:", modified_dict)
            results.append(modified_dict)
    return results


if __name__ == '__main__':

    device_set = sys.argv[1] if len(sys.argv) > 1 else "SET1"
    if device_set == "SET1" or device_set == "SET2" or device_set == "SET5":
        with open("device_details.json", "r") as jsonFile:
            device_data = json.load(jsonFile)
    elif device_set == "SET3":
        with open("device_details_set3.json", "r") as jsonFile:
            device_data = json.load(jsonFile)
    elif device_set == "SET4":
        with open("device_details_set4.json", "r") as jsonFile:
            device_data = json.load(jsonFile)

    start_time = round(time.time())

    change_routes()

    device_results = {}
    for key in device_data.keys():
        device_results[key] = []
    for key, value in device_data.items():
        print("*******************************" + key + "*****************************")
        if key == "Server":
            results = call_threading_process_servers(value)
        else:
            results = call_threading_process(value)
        device_results[key] = results

    end_time = round(time.time())
    total_seconds = end_time - start_time
    print("Task completed in {} minutes and {} seconds".format(total_seconds / 60, total_seconds % 60))

    with open("device_details_results.json", "w") as jsonFile:
        json.dump(device_results, jsonFile)

    print("Getting the clock on NTP servers for the given set")
    device_set = sys.argv[1] if len(sys.argv) > 1 else "SET1"
    if device_set == "SET1":
        print("Getting NTP Server clock for SET 1")
        try:
            telnet_login_check_status = check_telnet_login("175.175.30.1", "DNAC", "DNAC123", "DNAC123", "REAL",
                                                           "NTP")
            show_clock_output = telnet_login_check_status[1]
            ntp_server_clock_output = {
                "NTP_SERVER_IP":"175.175.30.1",
                "CLOCK_OUTPUT":show_clock_output
            }
        except Exception as e:
            error_message = ""
            if "connection refused" in str(e).lower():
                error_message = "Unable to fetch Clock - Connection Refused"
            elif "timeout exceeded" in str(e).lower():
                error_message = "Unable to fetch Clock - Connection Timeout Exceeded"
            else:
                error_message = "Unable to fetch Clock - Unknown Error"
            ntp_server_clock_output = {
                "NTP_SERVER_IP": "175.175.30.1",
                "CLOCK_OUTPUT": error_message,
                "RAW_ERROR":str(e)
            }
        with open('ntp_server_clock.json', 'w') as fp:
            json.dump(ntp_server_clock_output, fp)
    elif device_set == "SET2":
        print("Getting NTP Server clock for SET 2")
        try:
            telnet_login_check_status = check_telnet_login("175.175.30.98", "set2", "set2", "set2", "REAL",
                                                       "NTP")
            show_clock_output = telnet_login_check_status[1]
            ntp_server_clock_output = {
                "NTP_SERVER_IP": "175.175.30.98",
                "CLOCK_OUTPUT": show_clock_output
            }
        except Exception as e:
            error_message = ""
            if "connection refused" in str(e).lower():
                error_message = "Unable to fetch Clock - Connection Refused"
            elif "timeout exceeded" in str(e).lower():
                error_message = "Unable to fetch Clock - Connection Timeout Exceeded"
            else:
                error_message = "Unable to fetch Clock - Unknown Error"
            ntp_server_clock_output = {
                "NTP_SERVER_IP": "175.175.30.98",
                "CLOCK_OUTPUT": error_message,
                "RAW_ERROR": str(e)
            }
        with open('ntp_server_clock.json', 'w') as fp:
            json.dump(ntp_server_clock_output, fp)