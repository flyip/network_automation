#!/usr/bin/python3
import yaml
import os
from ncclient import manager
import requests
import json
import jinja2
import yaml
import logging


username = 'admin'
password = 'Huawei@123'
devices = yaml.load(open('../devices.yaml', 'r'), Loader=yaml.SafeLoader)
logs_dir = '../logs/'
header={'content-type':'application/json-rpc'}

def debug_REST():
  from http.client import HTTPConnection
  '''Switches on logging of the requests module.'''
  HTTPConnection.debuglevel = 1

  logging.basicConfig()
  logging.getLogger().setLevel(logging.DEBUG)
  requests_log = logging.getLogger("requests.packages.urllib3")
  requests_log.setLevel(logging.DEBUG)
  requests_log.propagate = True

def create_log_folder():
  if not os.path.exists(logs_dir):
    print('Creating logs directory')
    os.mkdir(logs_dir)
  else:
    print('Logs directory is existing')

def perform_nxos_cmd(hostname, ip, payload, username, password, header):
  url= 'https://' + ip +'/ins'
  #Send the command.
  logger.info(payload) #The command will be send to device.
  response = requests.post(url,data=json.dumps(payload), headers=header, auth=(username,password), verify=False).json()
  #Get the result
  for i in response:
    if 'error' in i:
      logger.error('NXOS task failed!')
    logger.info(json.dumps(i))

def perform_junos_cmd(hostname, ip, commands, username, password):
  #Send the command.
  conn = manager.connect(host=ip, \
                   port=830, \
                   username=username, \
                   password=password, \
                   timeout=60, \
                   device_params={'name': 'junos'}, \
                   hostkey_verify=False)
  #perform the task
  lock_result = conn.lock()
  conn.load_configuration(action='set', config=commands)
  conn.validate()
  conn.compare_configuration()
  conn.commit()
  conn.unlock()
  conn.close_session()

def make_cfg_nxos(data):
  bgp_cfg = jinja2.Environment(loader=jinja2.FileSystemLoader('../templates')).get_template('bgp_nxos.j2').render(data=data)
  interface_cfg = jinja2.Environment(loader=jinja2.FileSystemLoader('../templates')).get_template('interface_nxos.j2').render(data=data)
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
  return payload

def make_cfg_junos(data):
  bgp_cfg = jinja2.Environment(loader=jinja2.FileSystemLoader('../templates')).get_template('bgp_junos.j2').render(data=data)
  interface_cfg = jinja2.Environment(loader=jinja2.FileSystemLoader('../templates')).get_template('interface_junos.j2').render(data=data)
  merge = bgp_cfg + '\n' + interface_cfg
  commands = [ command for command in merge.split('\n') if command.strip() != '']
  return commands

if __name__ == "__main__":
  #Setting log.(info send to file, warining send to ternimal)
  logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', filename='../logs/myapp.log')
  logger = logging.getLogger()
  console = logging.StreamHandler()
  console.setLevel(logging.WARN)
  formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
  console.setFormatter(formatter)
  logging.getLogger('').addHandler(console)

  #Check the logs folder
  create_log_folder()

  #Let's start fun.
  for key in devices['device'].keys():
    hostname = devices['device'][key]['hostname']
    ip = devices['device'][key]['ip']
    url= 'https://' + ip +'/ins'
    platform = devices['device'][key]['platform']
    #Loading vars for each device.
    data = yaml.load(open('../vars/'+  hostname + '.yaml', 'r'), Loader=yaml.SafeLoader)
    print('*' * 20 + 'Starting ' + hostname + ' task' + '*' * 20)
    logger.info('*' * 20 + 'Starting ' + hostname + ' task' + '*' * 20 )
    if platform == 'junos':
      commands = make_cfg_junos(data)
      perform_junos_cmd(hostname, ip, commands, username, password)
    if platform == 'nxos':
      payload = make_cfg_nxos(data)
      #debug_REST()
      perform_nxos_cmd(hostname, ip, payload, username, password, header)
