#!/usr/bin/python3
import yaml
import os
from ncclient import manager
from ncclient.xml_ import new_ele, sub_ele
import requests
import json
import jinja2 
import yaml

vars = yaml.load(open('./vars/spine01.yaml', 'r'))
user = 'admin'
pw = 'Huawei@123'
data = yaml.load(open('./devices.yaml', 'r'))
logs_dir = './logs/'
myheaders={'content-type':'application/json-rpc'}




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


    if platform == 'nxos':
      vars = yaml.load(open('./vars/'+  hostname + '.yaml', 'r'))
      bgp_cfg = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates')).get_template('bgp_nxos.j2').render(data=vars)
      interface_cfg = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates')).get_template('interface_nxos.j2').render(data=vars)
      commands = interface_cfg + bgp_cfg 
      list = [command.strip() for command in commands.split('\n') if command.strip() != '']
      payload = []
      i = 1

      for abc in list:
        template = {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": abc,
          "version": 1
        },
        "id": i,
        "rollback": "rollback-on-error"
        }

        payload.append(template)
        i += 1 


      print('Starting ' + hostname)
      response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(user,pw), verify=False).json()
      f = open(logs_dir + hostname + '.json', 'w')

      for i in response:
        j = json.dumps(i) + '\n'
        f.write(j)
      f.close()


    if platform == 'junos':
      vars = yaml.load(open('./vars/'+  hostname + '.yaml', 'r'))
      print('Starting ' + hostname)

      conn = manager.connect(host=ip,
                       port=830,
                       username=user,
                       password=pw,
                       timeout=60,
                       device_params={'name': 'junos'},
                       hostkey_verify=False)
      
      lock_result = conn.lock()

      bgp_cfg = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates')).get_template('bgp_junos.j2').render(data=vars)
      interface_cfg = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates')).get_template('interface_junos.j2').render(data=vars)
      merge = bgp_cfg + '\n' + interface_cfg
      commands = [ command for command in merge.split('\n') if command.strip() != '']
      sethostname = 'set system host-name ' + hostname

      conn.load_configuration(action='set', config=sethostname)
      conn.load_configuration(action='set', config=commands)
      conn.load_configuration(action='set', config='set protocols lldp interface all ')
      print(conn.validate())
      print(conn.compare_configuration())
      conn.commit()
      conn.unlock()
      conn.close_session()

      