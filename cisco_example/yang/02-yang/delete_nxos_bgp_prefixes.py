#!/usr/bin/env python

from ncclient import manager
import sys
from lxml import etree
import logging
import sys

# Add parent directory to path to allow importing common vars

from device_info import sbx_n9kv_ao as device # noqa

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', stream='sys.stdout')  

# Loopback Info - Change the details for your interface
prefix = "10.99.99.0/24"

# create a main() method
def main():
    """
    Main method that removes a prefix from bgp
    """
    add_prefix = """ <config>
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <bgp-items>
            <inst-items>
                <dom-items>
                    <Dom-list>
                        <name>default</name>
                        <af-items>
                            <DomAf-list>
                                <type>ipv4-ucast</type>
                                <prefix-items>
                                    <AdvPrefix-list operation="remove">
                                        <addr>{}</addr>
                                    </AdvPrefix-list>
                                </prefix-items>
                            </DomAf-list>
                        </af-items>
                    </Dom-list>
                </dom-items>
            </inst-items>
        </bgp-items>
    </System>
    </config>""".format(prefix)

    with manager.connect(host = device["address"],
                         port = device["netconf_port"],
                         username = device["username"],
                         password = device["password"],
                         hostkey_verify = False) as m:

        # Add the prefix to BGP
        print("\nNow removing prefix {} from device {}..\n".format(prefix, device["address"]))
        netconf_response = m.edit_config(target='running', config=add_prefix)
        # Parse the XML response
        print(netconf_response)

if __name__ == '__main__':
    sys.exit(main())
