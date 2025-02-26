import json
import os
import smtplib
from email.mime.text import MIMEText
import sys

device_set = sys.argv[1] if len(sys.argv) > 1 else "SET1"

def send_mail(summary):
    msg = MIMEText(summary, 'html', _charset='utf-8')
    assert msg['Content-Transfer-Encoding'] == 'base64'

    SERVER = "outbound.cisco.com"
    FROM = "dnac-lab-support@cisco.com"
    if device_set == "SET2":
        TO = "spoolpan@cisco.com,rosalvi@cisco.com,suppurus@cisco.com,pmuthuva@cisco.com,nponnamb@cisco.com,vaisgurr@cisco.com,gkoshti@cisco.com,sakahuja@cisco.com,sudhhegd@cisco.com,lmisra@cisco.com,group.sranandr@cisco.com,group.karg@cisco.com,ba-regression@cisco.com,cshivapp@cisco.com,ntappa@cisco.com,sshettar@cisco.com,karachan@cisco.com,cmadraha@cisco.com,sranandr@cisco.com,nanramas@cisco.com,kaec@cisco.com,kumadeep@cisco.com,ramprabh@cisco.com,dnac-rma@cisco.com,phassang@cisco.com"
        msg['Subject'] = "DNAC VM Regression Device Status"

    elif device_set == "SET3":
        TO = "karachan@cisco.com,cmadraha@cisco.com,ramprabh@cisco.com,shantjai@cisco.com,sranandr@cisco.com,karanaku@cisco.com,sumullic@cisco.com,shwbiraj@cisco.com,bikabehe@cisco.com,phassang@cisco.com"
        msg['Subject'] = "BDD Device Status"

    elif device_set == "SET4":
        TO = "karachan@cisco.com,bikabehe@cisco.com,phassang@cisco.com,karanaku@cisco.com,aghantas@cisco.com,pkumarkb@cisco.com,kgnanend@cisco.com,madsaman@cisco.com,bdevadas@cisco.com"
        msg['Subject'] = "System Run Device Status"

    elif device_set == "SET5":
        TO = "karachan@cisco.com,bikabehe@cisco.com,phassang@cisco.com,karanaku@cisco.com,cmadraha@cisco.com"
        msg['Subject'] = "DevTest Pipeline Device Status"

    else:
        TO = "group.sranandr@cisco.com,group.karg@cisco.com,ba-regression@cisco.com,cshivapp@cisco.com,ntappa@cisco.com,sshettar@cisco.com,karachan@cisco.com,cmadraha@cisco.com,sranandr@cisco.com,nanramas@cisco.com,spoolpan@cisco.com,rosalvi@cisco.com,suppurus@cisco.com,pmuthuva@cisco.com,nponnamb@cisco.com,vaisgurr@cisco.com,gkoshti@cisco.com,sakahuja@cisco.com,sudhhegd@cisco.com,lmisra@cisco.com,kaec@cisco.com,kumadeep@cisco.com,ramprabh@cisco.com,dnac-rma@cisco.com,phassang@cisco.com"
        msg['Subject'] = "DNAC Production Device Status"

    msg['From'] = FROM
    msg['To'] = TO

    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO.split(','), msg.as_string())
    print("Successfully sent email")
    server.quit()


device_data = json.loads(open("device_details_results.json", "r").read())
telent_success = 0
telent_fail = 0
telent_status = []
ping_status = []
snmp_status = []
device_type = []
status_by_comp = []
srno = 0
total_device = 0
for key, value in device_data.items():
    total_device += len(value)
    ping_unreachable = []
    snmp_unreachable = []
    telnet_fail = []
    for i in range(len(value)):
        print(key)
        print(value)
        value_data = device_data[key][i]
        telent_status.append(value_data["telnet_status"])
        ping_status.append(value_data["ping_status"])
        snmp_status.append(value_data["snmp_status"])
        device_type.append(value_data['real/virtual'])

        if value_data["ping_status"] == "Unreachable":
            ping_unreachable.append(value_data["DEVICE_IP"])
        if value_data["snmp_status"] == "Unreachable":
            snmp_unreachable.append(value_data["DEVICE_IP"])
        if value_data["telnet_status"] != "Auth Success":
            telnet_fail.append(value_data["DEVICE_IP"])
    srno += 1
    status_by_comp.append([srno,key,len(value),len(ping_unreachable),len(snmp_unreachable),len(telnet_fail)])

for value in status_by_comp:
    if value[1] == "Server":
        value[-1] = 0

print("Telnet status")
print(telent_status.count("Auth Success"),telent_status.count("Auth Failed"))
print("Ping status")
print(ping_status.count("Reachable"),ping_status.count("Unreachable"))
print("Snmp status")
print(snmp_status.count("Reachable"),snmp_status.count("Unreachable"))
print("Device type count")
print(device_type.count("Real"),device_type.count("Sapro"),device_type.count("VIRL"),device_type.count("Virtual"))
print("Total number of Telnet fail")

server_devices = 0
if device_set == "SET1" or device_set == "SET2":
    print(len(device_data['Server']))
    server_devices = len(device_data['Server'])

total_telnet_fail = total_device - telent_status.count("Auth Success") - server_devices
print(total_telnet_fail)

Topo = open("ReportTopology.html", "w").close()

Summary = "<html><head><style>header {text-align: center;} table {border-collapse: collapse; margin: 0 auto;} table td{border: 1px solid #ddd; padding: 8px;} table tr:nth-child(even){background-color: #f2f2f2;} table th{pading: 8px; text-align: left;background-color: #4CAF50;color: white;}</style></head><header><b>DNAC Devices Reachability Summary</b></header><table class=dataframe><tr><th>Total</th><th>Ping Fail</th><th>SNMP Fail</th><th>Telnet Fail</th></tr>"
Summary_Comp = ("<tr><td>" + str(total_device) + "</td><td>" + str(ping_status.count("Unreachable")) + "</td><td>" + str(snmp_status.count("Unreachable"))
                + "</td><td>"+ str(total_telnet_fail) +"</td></tr></table><div></div>")
Summary = Summary + Summary_Comp

Summary_Comp = "<p></p><header><b>DNAC Production Devices</b></header><table class=dataframe><tr><th>Total</th><th>Real</th><th>Sapro</th><th>VIRL</th><th>Virtual</th><th>Servers</th></tr>"
Summary = Summary + Summary_Comp
Summary_Comp = "<tr><td>" + str(total_device) + "</td><td>" + str(device_type.count("Real")) + "</td><td>" + str(
    device_type.count("Sapro")) + "</td><td>" + str(device_type.count("VIRL")) + "</td><td>" + str(device_type.count("Virtual")) + "</td><td>" + str(server_devices) + "</td></tr></table><div></div>"
Summary = Summary + Summary_Comp

Topo = open("ReportTopology.html", 'a')
Topo.write(Summary)
Topo.close()


# ntp_server_info = json.loads(open("ntp_server_clock.json","r").read())
# ntp_server_html = "<p></p><header><b>NTP Server</b></header><table class=dataframe><tr><th>NTP Server IP</th><th>Clock</th></tr><tr><td>"+ntp_server_info["NTP_SERVER_IP"]+"</td><td>"+ntp_server_info["CLOCK_OUTPUT"]+"</td></tr></table><p></p>"
# Summary = Summary + ntp_server_html

Summary_Comp = "<p></p><header><b> Component Devices Reachability Summary </b></header><table class=dataframe><tr><th>Sr.No</th><th>Component</th><th>Total Devices</th><th>Ping Unreachable</th><th>SNMP Unreachable</th><th>Telnet Authentication Failed</th>"
Summary = Summary + Summary_Comp

for comp in status_by_comp:
    Summary_Comp = "<tr><td>" + str(comp[0]) + "</td><td>" + str(comp[1]) + "</td><td>" + str(
        comp[2]) + "</td><td>" + str(comp[3]) + "</td><td>" + str(comp[4]) + "</td><td>" + str(comp[5]) + "</td></tr>"
    Summary = Summary + Summary_Comp
Summary = Summary + "</table><p></p></html>"

ntp_server_info = json.loads(open("ntp_server_clock.json","r").read())
ntp_server_html = "<p></p><header><b>NTP Server</b></header><table class=dataframe><tr><th>NTP Server IP</th><th>Clock</th></tr><tr><td>"+ntp_server_info["NTP_SERVER_IP"]+"</td><td>"+ntp_server_info["CLOCK_OUTPUT"]+"</td></tr></table><p></p>"
Summary = Summary + ntp_server_html


for key,value in device_data.items():
    y = 0
    Comphtml = "<html><header><b>" + key + "</b></header><table><tr><th>Sr.No</th><th>Device Type</th><th>Real/SIM</th><th>Device Model</th><th>IP Address</th><th>Ping</th><th>SNMP</th><th>Telnet Status</th><th>Device Image</th><th>Device Clock</th></tr>"
    for i in range(len(value)):
        value_data = device_data[key][i]
        # print(value_data)
        y = y + 1
        WriteTable = "<tr><td>" + str(y) + "</td><td>" + value_data['device_type'] + "</td><td>" + value_data['real/virtual'] + "</td><td>" + \
                         value_data['device_model'] + "</td><td>" + value_data['DEVICE_IP'] + "</td><td bgcolor=" + value_data['ping_font'] + ">" + \
                         value_data['ping_status'] + "</td><td bgcolor=" + value_data['snmp_font'] + ">" + value_data['snmp_status'] + \
                         "</td><td bgcolor="+value_data['telnet_font']+">"+value_data['telnet_status']+ \
                      "</td><td>"+value_data['device_image']+"</td><td>"+value_data['show_clock']+"</td></tr>"
        Comphtml = Comphtml + WriteTable

    Comphtml = Comphtml + "</table><p></p></html>"
    Summary = Summary + Comphtml

Summary = Summary + "</html>"
Topo = open("ReportTopology.html", 'w')
Topo.write(Summary)
Topo.close()

with open("ReportTopology.html","r") as fo:
    send_mail(fo.read())

def add_set1_routes():
    routes_delete = ["sudo -S route del -net 175.175.0.0/16", "sudo -S route del -net 48.0.0.0/8",
                     "sudo -S route del -net 35.1.1.0/24"]
    routes_set1 = ["sudo -S route add -net 175.175.0.0/16 gw 175.175.40.1",
                   "sudo -S route add -net 48.0.0.0/8 gw 175.175.40.1",
                   "sudo -S route add -net 35.1.1.0/24 gw 175.175.40.1"]

    for route in routes_delete:
        print(os.system("echo cisco123 | {}".format(route)))
    print("Done deleting existing routes")

    for route in routes_set1:
        print(os.system("echo cisco123 | {}".format(route)))

add_set1_routes()