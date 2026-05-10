import subprocess
import json
import socket
import datetime

services = ["httpd", "rabbitmq", "postgresql"]
hostname = socket.gethostname()
app_is_up = True

for s in services:
    result = subprocess.run(["systemctl", "is-active", s], capture_output=True, text=True)

    if result.stdout.strip() == "active":
        status = "UP"
    else:
        status = "DOWN"
        app_is_up = False

    data = {}
    data["service_name"] = s
    data["service_status"] = status
    data["host_name"] = hostname

    now = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = s + "-status-" + now + ".json"

    f = open(filename, "w")
    json.dump(data, f)
    f.close()
    print("written: " + filename)

if app_is_up == True:
    print("rbcapp1 is UP")
else:
    print("rbcapp1 is DOWN")
