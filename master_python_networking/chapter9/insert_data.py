#!/usr/bin/python3

import requests
import yaml
import logging

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

for device in data['device'].keys():
    hostname = data['device'][device]['hostname']
    loopback = data['device'][device]['lo0']
    mgmt_ip = data['device'][device]['ip']
    vendor = data['device'][device]['verndor']
    os = data['device'][device]['version']
    role = data['device'][device]['role']
    #if hostname == 'spine01':
    create_device(hostname=hostname, loopback=loopback, mgmt_ip=mgmt_ip, vendor=vendor, os=os, role=role)

