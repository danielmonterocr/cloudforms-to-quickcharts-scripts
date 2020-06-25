import json
import requests
from quickchart import QuickChart
import webbrowser

current_token=json.loads(requests.get('https://10.99.92.141/api/auth',auth=("admin",'passw0rd'),verify=False).text)['auth_token']

response=json.loads(requests.get('https://10.99.92.141/api/results?filter[]=name="Total Cost Providers"&sort_by=id&sort_order=desc&offset=0&limit=1&expand=resources',headers={'X-Auth-Token' : current_token},verify=False).text)
result_set=response['resources'][0]['result_set']

total_per_day_amazon = []
total_per_day_azure = []
total_per_day_vcenter = []
num_days_report = 7

for result in result_set:
    if (result['tag_name'] == 'AWS'):
        total_per_day_amazon.append(result['total_cost'])
    elif (result['tag_name'] == 'Azure'):
        total_per_day_azure.append(result['total_cost'])
    elif (result['tag_name'] == 'vSphere'):
        total_per_day_vcenter.append(result['total_cost'])

total_per_day_amazon = total_per_day_amazon[-num_days_report:]
total_per_day_azure = total_per_day_azure[-num_days_report:]
total_per_day_vcenter = total_per_day_vcenter[-num_days_report:]

zero_list = [0] * (num_days_report - len(total_per_day_amazon))
total_per_day_amazon = zero_list + total_per_day_amazon
zero_list = [0] * (num_days_report - len(total_per_day_azure))
total_per_day_azure = zero_list + total_per_day_azure
zero_list = [0] * (num_days_report - len(total_per_day_vcenter))
total_per_day_vcenter = zero_list + total_per_day_vcenter

# Downscale vCenter costs
new_total_per_day_vcenter = []
for total in total_per_day_vcenter:
    new_total_per_day_vcenter.append(float(total) / 100)

print(total_per_day_amazon)
print(total_per_day_azure)
#print(total_per_day_vcenter)
print(new_total_per_day_vcenter)

qc = QuickChart()
qc.width = 500
qc.height = 300
qc.device_pixel_ratio = 2.0
qc.config = {
    "type": "bar",
    "data": {
        "labels": ["18/06/2020","19/06/2020","20/06/2020","21/06/2020","22/06/2020","23/06/2020","24/06/2020"],
        "datasets": [
            {
                "label": "Amazon",
                "backgroundColor": "rgb(216,27,96)",
                "data": total_per_day_amazon,
            },
            {
                "label": "Azure",
                "backgroundColor": "rgb(255,193,7)",
                "data": total_per_day_azure,
            },
            {
                "label": "vCenter",
                "backgroundColor": "rgb(30,136,229)",
                "data": new_total_per_day_vcenter,
            }
        ]
    },
    "options": {
        "title": {
            "display": "true",
            "text": "Total Cost by Providers",
        },
        "scales": {
            "xAxes": [
                {
                    "stacked": "true",
                },
            ],
            "yAxes": [
                {
                    "stacked": "true",
                },
            ]
        }
    }
}

# Print the chart URL
#print(qc.get_url())

webbrowser.open(qc.get_url())
