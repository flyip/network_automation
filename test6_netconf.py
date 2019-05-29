#!/usr/bin/python3

from ncclient import manager
from ncclient.xml_ import new_ele, sub_ele
import yaml
import os
import requests
import json

user = 'admin'
pw = 'Huawei@123'
data = yaml.load(open('devices.yaml', 'r'))
commands = yaml.load(open('commands1.yaml', 'r'))
rpc = """
<rpc>
    <get-interface-information>
    </get-interface-information>
</rpc>
"""



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
        #lock configuration.
        conn.lock

        #Build configration
        config = new_ele('system')
        sub_ele(config, 'host-name').text = 'vmx'

        #Upload , validate, and commit configuration 
        conn.load_configuration(config=config)
        conn.validate()
        commit_config = conn.commit()
        print(commit_config.tostring)

        #unlock config
        #conn.unlock
        
        #result = conn.rpc(rpc)
        #print(result)
        # close session
        conn.close_session()