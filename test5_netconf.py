#!/usr/bin/python3

from ncclient import manager
import yaml
import os
import requests
import json

user = 'admin'
pw = 'Huawei@123'
data = yaml.load(open('devices.yaml', 'r'))
commands = yaml.load(open('commands1.yaml', 'r'))


for key in data['device'].keys():

    hostname = data['device'][key]['hostname']
    ip = data['device'][key]['ip']
    platform = data['device'][key]['platform']
    if platform == 'vmx':
        conn = manager.connect(
            host = ip,
            port = 830,
            username = user,
            password = pw,
            timeout = 10,
            device_params = {'name' : 'junos'},
            hostkey_verify = False
            )
        #Backup configuration   
        #c = conn.get_config(source='running').data_xml
        #with open("%s.xml" % hostname, 'w') as f:
        #    f.write(c)

        c = conn.dispatch('clear-arp-table')
        print(c)


        #Close the NETCONF session
        conn.close_session()

