#!/usr/bin/python3
import sys
import time
import select
import paramiko
import yaml

user = 'admin'
pw = 'Huawei@123'
i = 1
data = yaml.load(open('devices.yaml', 'r'))
commands = yaml.load(open('commands.yaml', 'r'))

for key in data['device'].keys():

    hostname = data['device'][key]['hostname']
    ip = data['device'][key]['ip']

    while True:
        print("Trying to connect to %s (%i/30)" % (ip, i))
        try:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=user, password=pw)
            print("Connected to %s" % hostname)
            break
        except paramiko.AuthenticationException:
            print("Authentication failed when connecting to %s" % hostname)
            sys.exit(1)
        except:
            print("Could not SSH to %s, waiting for it to start" % hostname)
            i += 1
            time.sleep(2)
        # If we could not connect within time limit
        if i == 30:
            print("Could not connect to %s. Giving up" % hostname)
            sys.exit(1)
        
    # Send the command (non-blocking)
    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command)
        # Wait for the command to terminate
        while not stdout.channel.exit_status_ready():
            # Only print data if there is data to read in the channel
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    # Print data from stdout
                    print(stdout.channel.recv(1024))
    #
    # Disconnect from the host
    #
    print("Command done, closing SSH connection")
    ssh.close()