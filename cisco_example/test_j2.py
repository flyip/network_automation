#!/usr/bin/python3
from jinja2 import Template
import yaml
import re

data = yaml.load(open('/home/fly/Documents/python_networking/vars/spine01.yaml', 'r'))
#generate bgp config
interface_template = Template('''
{% for interface in data['interfaces'].keys() -%}
{% if 'lo' not in interface -%}
interface {{interface}}
  {% if data['interfaces'][interface]['Layer'] %}no switchport{% endif %}
  ip address {{data['interfaces'][interface]['IP']}}
  {{data['interfaces'][interface]['State']}}
  exit
{% endif -%}
{% if 'lo' in interface -%}
interface {{interface}}
  ip address {{data['interfaces'][interface]['IP']}}
  exit
{% endif -%}
{% endfor %}''')
#generate bgp config
bgp_template = Template('''router bgp {{data['protocols']['bgp']['local_as']}}
  router-id {{data['protocols']['bgp']['RID']}}
  address-family {{data['protocols']['bgp']['address_family']}}
  {%- for network in data['protocols']['bgp']['advertise_subnets'] %}
  network {{network}}
  {%- endfor -%}
  {%- for peer in data['protocols']['bgp']['peers'].keys() %}
  neighbor {{peer}} 
    remote-as {{data['protocols']['bgp']['peers'][peer]}}
    address-family ipv4 unicast
    exit
    exit
  {%- endfor %}''')

commands = interface_template.render(data=data) + bgp_template.render(data=data)

#list = [command.strip() for command in commands.split('\n') if command.strip() != '']
print(commands.strip().replace('\n', ';'))