#!/usr/bin/python3

import requests
import yaml
import logging
import random

data = yaml.load(open('devices.yaml'),Loader=yaml.SafeLoader)

def debug_REST():
    from http.client import HTTPConnection
    '''Switches on logging of the requests module.'''
    HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def create_device(hostname, loopback, mgmt_ip, vendor, os, role):
    #debug_REST()
    r = requests.post('http://127.0.0.1:5000/devices/', json = {'hostname':hostname, 'loopback':loopback, 'mgmt_ip': mgmt_ip, 'vendor': vendor, 'os': os, 'role': role})
    print(r.request.body)
    print(r.text)
    #print(hostname, loopback, mgmt_ip, vendor,os, role)

#def query_device()

for i in range(4,254):
    if i <= 16:
        if i < 10:
            hostname = 'spine0' + str(i)
        else:
            hostname = 'spine' + str(i)
    else:
        hostname = 'leaf' + str(i)
        loopback = '192.168.0.' + str(i)
        mgmt_ip = '192.168.122.' + str(i)
        vendor = random.choice(['cisco', 'juniper'])
        os = random.choice(['9.2.3', '17.1R1.8'])
        role = random.choice(['spine', 'leaf'])
        print(hostname, loopback, mgmt_ip, vendor,os, role)
    #if hostname == 'spine01':
        create_device(hostname=hostname, loopback=loopback, mgmt_ip=mgmt_ip, vendor=vendor, os=os, role=role)

