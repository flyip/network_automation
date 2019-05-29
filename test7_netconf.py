
#!/usr/bin/env python
import logging
import sys

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
        <get-interface-information>
                <interface-name>ge-0/0/0</interface-name>
        </get-interface-information>
    """

    result = conn.rpc(rpc)
    f.write(result.data_xml)
    f.close()
    conn.close_session()


if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)

connect('spine02', 830, 'admin', 'Huawei@123')
