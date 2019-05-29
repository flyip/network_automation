#!/usr/bin/python3
import yaml
import os
from ncclient import manager
import requests
import json
import jinja2 
import yaml
import logging

vars = yaml.load(open('./vars/spine01.yaml', 'r'), Loader=yaml.SafeLoader)
user = 'admin'
pw = 'Huawei@123'
data = yaml.load(open('./devices.yaml', 'r'), Loader=yaml.SafeLoader)
logs_dir = './logs/'
myheaders={'content-type':'application/json-rpc'}



logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', filename='./logs/myapp.log')    
logger = logging.getLogger()
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.WARN)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console) 


#create logs directory
print('Check logs directory!')
if not os.path.exists(logs_dir):
    print('Creating logs directory')
    os.mkdir(logs_dir)
    
else:
    print('Logs directory is existing')

#Get device vars
for key in data['device'].keys():

    hostname = data['device'][key]['hostname']
    ip = data['device'][key]['ip']
    url= 'https://' + ip +'/ins'
    platform = data['device'][key]['platform']

    #perform NXOS task
    if platform == 'nxos':
      logger.warning('*'*20 + 'Starting ' + hostname + '*'*20 )
      vars = yaml.load(open('./vars/'+  hostname + '.yaml', 'r'), Loader=yaml.SafeLoader)

      #generate the configuration
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
      #Send REST request to NE.
      response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(user,pw), verify=False).json()

      logger.info(payload)

      #Get the result
      for i in response:
        if 'error' in i:
          logger.error('NXOS task failed!')
        logger.info(json.dumps(i))

    #perform JUNOS task
    if platform == 'junos':
      logger.warning('*'*20 + 'Starting ' + hostname + '*'*20 )
      vars = yaml.load(open('./vars/'+  hostname + '.yaml', 'r'), Loader=yaml.SafeLoader)

      conn = manager.connect(host=ip,
                       port=830,
                       username=user,
                       password=pw,
                       timeout=60,
                       device_params={'name': 'junos'},
                       hostkey_verify=False)

      #Generate the configuration 
      bgp_cfg = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates')).get_template('bgp_junos.j2').render(data=vars)
      interface_cfg = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates')).get_template('interface_junos.j2').render(data=vars)
      merge = bgp_cfg + '\n' + interface_cfg
      commands = [ command for command in merge.split('\n') if command.strip() != '']

      #perform the task
      lock_result = conn.lock()
      conn.load_configuration(action='set', config=commands)
      conn.commit()
      conn.unlock()
      conn.close_session()

      