
#!/usr/bin/env python
import logging
import sys

from ncclient import manager


def connect(host, port, user, password, command):
    with manager.connect(
        host=host,
        port=port,
        username=user,
        password=password,
        timeout=60,
        device_params={'name': 'junos'},
        hostkey_verify=False
    ) as m:
        with m.locked('candidate'):
            result = m.load_configuration(action='set', config=command)
            logging.info(result)
            result = m.commit()
            logging.info(result)


if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)

    connect('spine02', 830, 'admin', 'Huawei@123', 'set interfaces fxp0 description MGMT_IF')