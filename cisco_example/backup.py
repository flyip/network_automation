#! /usr/bin/env python3

from ncclient import manager
from ncclient.xml_ import new_ele, sub_ele
import logging
import sys

add_ip_interface = """<config>
<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
  <ipv4-items>
    <inst-items>
      <dom-items>
        <Dom-list>
          <name>default</name>
          <if-items>
            <If-list>
              <id>lo9</id>
              <addr-items>
                <Addr-list>
                  <addr>9.9.9.1/32</addr>
                </Addr-list>
              </addr-items>
            </If-list>
          </if-items>
        </Dom-list>
      </dom-items>
    </inst-items>
  </ipv4-items>
  <intf-items>
    <lb-items>
      <LbRtdIf-list>
        <id>lo9</id>
        <adminSt>up</adminSt>
      </LbRtdIf-list>
    </lb-items>
  </intf-items>
</System>
</config>"""

def connect(host, port, user, password):
    conn = manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           timeout=60,
                           device_params={'name': 'nexus'},
                           hostkey_verify=False)   

    lock_result = conn.lock()
    logging.warning(lock_result)
    #result = conn.get(('subtree', loopback_filter))
    result = conn.edit_config(target='running', config=add_ip_interface)
    logging.warning(result)
    

    unlock_result = conn.unlock()
    logging.warning(unlock_result)
    conn.close_session()
    logging.warning('Didconnect to NE!')
    #print(conn.compare_configuration())
    #print(result.data_xml)

if __name__ == '__main__':
    file_handler = logging.FileHandler(filename='./logs/myapps.log')
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', handlers=handlers)
    connect('spine01', 830, 'admin', 'Huawei@123')
