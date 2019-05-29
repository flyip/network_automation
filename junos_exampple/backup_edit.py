#!/usr/bin/env python
import logging

from ncclient import manager
from ncclient.xml_ import *

config_filter = new_ele('configuration')
system_ele = sub_ele(config_filter, 'system')
sub_ele(system_ele, 'services')

def connect(host, port, user, password):
    conn = manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           timeout=60,
                           device_params={'name': 'junos'},
                           hostkey_verify=False)

    running = conn.get_configuration(source='running')
    dir(running.data_xml)

if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)
    
    connect('spine01', 830, 'admin', 'Huawei@123')