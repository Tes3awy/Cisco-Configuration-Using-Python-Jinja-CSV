#!/usr/bin/env python

# -----------------------------------------------------------------------------
#
# Demonstrates how to generate Cisco configuration using Python, Jinja2 and CSV
#
# (C) 2021 Osama Abbas, Cairo, Egypt
# Released under MIT License
#
# Filename: cisco_config_generator.py
# Version: Python 3.9.4
# Authors: Osama Abbas (oabbas2512@gmail.com)
# Description:   The program is designed to generate a configuration template
#                for Cisco Catalyst switches.
#
# -----------------------------------------------------------------------------

# Libraries
from os import path, mkdir, stat
from csv import DictReader
from jinja2 import Environment, FileSystemLoader
import json
import webbrowser as TextEditor
from time import sleep

# Global Vars
jinja_template = "switch.j2"
output_dir = "configs"
params_file = "params.csv"
vlans_file = "vlans.csv"
etherchannels_file = "etherchannels.csv"
port_mapping = "port_mapping.csv"

# Handle Jinja template
env = Environment(loader=FileSystemLoader("./"), trim_blocks=True, lstrip_blocks=True)
template = env.get_template(jinja_template)

# Create configs directory if not already created
if not path.exists(output_dir):
    mkdir(output_dir)

# Read the "parameters" csv sheet and convert it to a dict
with open(params_file, "r") as parameters:
    params = DictReader(parameters)
    for param in params:
        dict_params = dict(param)

# Read the "vlans" csv sheet and convert it to a dict
with open(vlans_file, "r") as vlans:
    vlans = DictReader(vlans)
    dict_vlans = {"vlans": []}
    for vlan in vlans:
        dict_vlans["vlans"].append(dict(vlan))

# Read the "etherchannels" csv sheet and convert it to a dict
with open(etherchannels_file, "r") as etherchannels:
    portchannels = DictReader(etherchannels)
    dict_portchannels = {"etherchannels": []}
    for portchannel in portchannels:
        dict_portchannels["etherchannels"].append(dict(portchannel))

# Read the "port mapping" csv sheet and convert it to a dict
with open(port_mapping, "r") as interfaces:
    ports = DictReader(interfaces)
    dict_ports = {"interfaces": []}
    for port in ports:
        dict_ports["interfaces"].append(dict(port))

# Combine all four csv sheets
dict_params.update(dict_vlans)
dict_params.update(dict_portchannels)
dict_params.update(dict_ports)

# All dictionaries
dicts = dict_params

# Generate the configuration template file
res = template.render(dicts)
file_name = dicts["hostname"]
file_ext = ".ios"
file_location = path.join(output_dir, file_name + file_ext)
file = open(file_location, "w")
file.write(res)
file.close()

print("✔ Configuration file '%s' is created successfully!" % (file_name + file_ext))

# Open file in default Text Editor for the file extension
sleep(1)
TextEditor.open(file_location)