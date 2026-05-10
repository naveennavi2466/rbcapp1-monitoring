# rbcapp1 Monitoring Assignment

## Overview

rbcapp1 depends on three services: httpd, rabbitmq, and postgresql.
If any one of them is down, rbcapp1 is considered DOWN.

## Files

| File | Description |
|------|-------------|
| monitor.py | Checks each service and writes a JSON status file per service |
| app.py | Flask REST API with /add and /healthcheck endpoints |
| inventory | Ansible inventory with 3 separate hosts |
| assignment.yml | Ansible playbook supporting 3 actions |
| process_sales.py | Filters real estate CSV to below-average price per sqft |

## How to run TEST1

Install dependencies:
```
pip install flask elasticsearch
```

Run the monitor script:
```
python monitor.py
```

Start the REST API:
```
python app.py
```

Endpoints:
- POST /add
- GET /healthcheck
- GET /healthcheck/{serviceName}

## How to run TEST2

Install Ansible:
```
pip install ansible
```

Update the IP addresses and alert_email in the inventory file, then run:
```
ansible-playbook assignment.yml -i inventory -e action=verify_install
ansible-playbook assignment.yml -i inventory -e action=check-disk
ansible-playbook assignment.yml -i inventory -e action=check-status
```

## How to run TEST3

Place sales-data.csv in the same folder, then run:
```
python process_sales.py
```

Output will be saved to below-average-sales.csv
