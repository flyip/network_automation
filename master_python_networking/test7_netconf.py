
#!/usr/bin/env python
import logging
import sys
from bs4 import BeautifulSoup

from ncclient import manager
f = open('result.xml', 'w')

def connect(host, port, user, password):
    conn = manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           timeout=60,
                           device_params={'name': 'junos'},
                           hostkey_verify=False)

    rpc = """
        <get-bgp-neighbor-information>
                <neighbor-address>10.0.0.7</neighbor-address>
        </get-bgp-neighbor-information>
    """

    result = conn.rpc(rpc)
    soup = BeautifulSoup(str(result), 'xml')
    print(soup.find('output-octets').text)
    conn.close_session()

if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    #logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)

connect('spine02', 830, 'admin', 'Huawei@123')
