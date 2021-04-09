#!/usr/bin/env python

# --------------------------------------------------------------------------------------
#
# Demonstrates how to generate Cisco configuration template using Python, Jinja2 and CSV
#
# (C) 2021 Osama Abbas, Cairo, Egypt
# Released under MIT License
#
# Filename: cisco_config_generator.py
# Version: Python 3.9.4
# Authors: Osama Abbas (oabbas2512@gmail.com)
# Description:   This program is designed to generate a configuration template
#                for Cisco Catalyst switches.
#
# --------------------------------------------------------------------------------------

# Libraries
from os import path, mkdir, stat
from csv import DictReader
from jinja2 import Environment, FileSystemLoader
import webbrowser as TextEditor
from time import sleep

# Global Vars
OUTPUT_DIR = "configs"
JINJA_TEMPLATE = "switch.j2"
PARAMS_FILE = "CSV/01. params.csv"
VLANS_FILE = "CSV/02. vlans.csv"
ETHERCHANNELS_FILE = "CSV/03. etherchannels.csv"
PORT_MAPPING = "CSV/04. port_mapping.csv"


def build_template(
    template_file, parameters_file, vlans_file, etherchannels_file, port_mapping
):

    # Handle Jinja template
    env = Environment(
        loader=FileSystemLoader("./"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template(JINJA_TEMPLATE)

    # Create configs directory if not already created
    if not path.exists(OUTPUT_DIR):
        mkdir(OUTPUT_DIR)

    # Read the "parameters" csv sheet and convert it to a dict
    with open(PARAMS_FILE, "r") as parameters:
        params = DictReader(parameters)
        for param in params:
            dict_params = dict(param)

    # Read the "vlans" csv sheet and convert it to a dict
    with open(VLANS_FILE, "r") as vlans:
        vlans = DictReader(vlans)
        dict_vlans = {"vlans": []}
        for vlan in vlans:
            dict_vlans["vlans"].append(dict(vlan))

    # Read the "etherchannels" csv sheet and convert it to a dict
    with open(ETHERCHANNELS_FILE, "r") as etherchannels:
        portchannels = DictReader(etherchannels)
        dict_portchannels = {"etherchannels": []}
        for portchannel in portchannels:
            dict_portchannels["etherchannels"].append(dict(portchannel))

    # Read the "port mapping" csv sheet and convert it to a dict
    with open(PORT_MAPPING, "r") as interfaces:
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
    file_location = path.join(OUTPUT_DIR, file_name + file_ext)
    file = open(file_location, "w")
    file.write(res)
    file.close()

    print("✔ Configuration file '%s' is created successfully!" % (file_name + file_ext))

    # Open file in default Text Editor for the file extension
    sleep(1)
    TextEditor.open(file_location)
    return True


if __name__ == "__main__":
    build_template(
        JINJA_TEMPLATE, PARAMS_FILE, VLANS_FILE, ETHERCHANNELS_FILE, PORT_MAPPING
    )
