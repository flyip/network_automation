#!/usr/bin/python3
import yaml
import os
from ncclient import manager
import requests
import json
import logging
import sys
import logging
import contextlib
from http.client import HTTPConnection

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

#Debug request
def debug_requests_on():
    '''Switches on logging of the requests module.'''
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def debug_requests_off():
    '''Switches off logging of the requests module, might be some side-effects'''
    HTTPConnection.debuglevel = 0

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    root_logger.handlers = []
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = False

@contextlib.contextmanager
def debug_requests():
    '''Use with 'with'!'''
    debug_requests_on()
    yield
    debug_requests_off()

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
    url= 'https://' + ip +'/ins'
    platform = data['device'][key]['platform']

    if hostname == 'spine01':
      debug_requests_on()
      print('Starting ' + hostname)
      response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(user,pw), verify=False).json()
      #response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(user,pw)).json()
      print(response['result'])

 










