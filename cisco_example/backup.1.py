#! /usr/bin/env python3

from ncclient import manager
from ncclient.xml_ import new_ele, sub_ele
import logging
import sys
import xml.etree.ElementTree as ET
from ncclient.xml_ import to_ele

add_ip_interface = """<config>
<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
  <intf-items>
    <phys-items>
      <PhysIf-list>
        <id>eth1/2</id>
        <adminSt>up</adminSt>
        <descr>NETCONF</descr>
        <layer>Layer3</layer>
        <userCfgdFlags>admin_state</userCfgdFlags>
      </PhysIf-list>
    </phys-items>
  </intf-items>
  <ipv4-items>
    <inst-items>
      <dom-items>
        <Dom-list>
          <name>default</name>
          <if-items>
            <If-list>
              <id>eth1/2</id>
              <addr-items>
                <Addr-list>
                  <addr>10.0.0.2/31</addr>
                </Addr-list>
              </addr-items>
            </If-list>
          </if-items>
        </Dom-list>
      </dom-items>
    </inst-items>
  </ipv4-items>
</System>
</config>"""

command1={'show vlan'}

rpc = '''
      <show xmlns="http://www.cisco.com/nxos:1.0:vlan_mgr_cli">
        <vlan>
          <brief/>
        </vlan>
      </show> 
'''

def connect(host, port, user, password):
    conn = manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           timeout=60,
                           device_params={'name': 'nexus'},
                           hostkey_verify=False)   

  
    #result = conn.edit_config(target='running', config=add_ip_interface)
    #conn.copy_config(source='running', target='candidate')
    conn.dispatch(to_ele(rpc))
    #conn.rpc(save)
    #conn.unlock(target='running')
    conn.close_session()
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', filename='./logs/myapp.log')    
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console) 

    connect('spine01', 830, 'admin', 'Huawei@123')
