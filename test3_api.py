#!/usr/bin/python3
import yaml
import os
from ncclient import manager
import requests
import json

user = 'admin'
pw = 'Huawei@123'
data = yaml.load(open('devices.yaml', 'r'))
commands = yaml.load(open('commands.yaml', 'r'))
logs_dir = '/home/fly/Documents/python_networking/logs/'
myheaders={'content-type':'application/json-rpc'}
payload=[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show version",
      "version": 1.2
    },
    "id": 1
  }
]  

#create logs directory
print('Check logs directory!')
if not os.path.exists(logs_dir):
    print('Creating logs directory')
    os.mkdir(logs_dir)
    
else:
    print('Logs directory is existing')


for key in data['device'].keys():

    hostname = data['device'][key]['hostname']
    ip = data['device'][key]['ip']
    url= 'http://' + ip +'/ins'

    print('Starting ' + hostname)
    response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(user,pw)).json()
    print(response['result'])

 










