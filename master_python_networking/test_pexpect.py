#!/usr/bin/python3
import pexpect
import sys
import yaml
import os

username = 'admin'
password = 'Huawei@123'
logs_dir = '/home/fly/Documents/python_networking/logs/'
data = yaml.load(open('devices.yaml', 'r'))

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

    fout = open(logs_dir + hostname + '.log','w')

    ssh = pexpect.spawn('ssh ' + username + '@' + ip, encoding='utf-8')
    ssh.logfile = fout
    ssh.expect('[Pp]assword:')
    ssh.sendline(password)
    ssh.expect('#')
    ssh.sendline('show clock ')
    ssh.expect('#')
    ssh.sendline('config t')
    ssh.expect('\(config\)#')
    ssh.sendline('hostname ' + hostname)
    ssh.expect('\(config\)#')
    ssh.sendline('exit')
    ssh.expect('#')
    ssh.sendline('show hostname')
    ssh.expect('#')
    ssh.close()
    ssh.logfile.close()
    fout.close()
    ssh.isalive()
