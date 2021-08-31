#!/usr/bin/env python3
#-----------------------------------------------------------------------
# Simple script to connect with SSH to NOKIA / ALCATEL OLTs ISAN FX8, FX16
#-----------------------------------------------------------------------

__author__ = 'Felipe Lira'
__version__= 1.0

# import netmiko library
from netmiko import ConnectHandler
from datetime import datetime

# create paramiters of connections
nokia = {
	'device_type': 'alcatel_aos',
	'host': '10.10.10.10', #IP OLT
	'username': 'user',  #User OLT
	'password': 'user@1234', #Pass OLT
	}

# Connect to OLT
net_connect = ConnectHandler(**nokia)

# show terminal to prove connection
net_connect.find_prompt()


# Insert serial the ONT
mac = input("Informe o serial da ONU (ALCLxxxx): ")
serial_onu = mac[4:].upper()

# Inhibit alarms the ssh conection
inhibit_alarms = net_connect.send_config_set('environment inhibit-alarms')

# Find equipment by serial_numer (ALCLxxx)
find_equipment = net_connect.send_command(f'show equipment ont status pon | match exact:ALCL:{serial_onu}')


if f'ALCL:{serial_onu}' in find_equipment:
    #shutdown and remove ONU/ONT
    interface = find_equipment.split()
    interface_onu = interface[1]
    shut_onu = net_connect.send_config_set(f'configure equipment ont interface {interface_onu} admin-state down')
    del_onu = net_connect.send_config_set(f'configure equipment ont no interface {interface_onu}')
    print('ONU desautorizada com sucesso')

else:
    print('ONU nao localizada!')

# disconect ssh connection
net_connect.disconnect()
