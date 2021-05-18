#!/usr/bin/env python3

# ---------------------------------------------------------------------------------------
#
# Demonstrates how to generate Cisco configuration template using Python3, Jinja2 and CSV
#
# (C) 2021 Osama Abbas, Cairo, Egypt
# Released under MIT License
#
# Filename: cisco_config_generator.py
# Version: Python 3.9.4
# Authors: Osama Abbas (oabbas2512@gmail.com)
# Description:   This program is designed to generate a configuration template
#                for Cisco Catalyst/Nexus switches.
#
# ---------------------------------------------------------------------------------------

# Libraries
import json
import webbrowser as TextEditor
from csv import DictReader
from datetime import date, datetime
from os import mkdir, path
from time import sleep

from colorama import init
from jinja2 import Environment, FileSystemLoader
from termcolor import cprint

from cisco_validation import validate_cisco_config

init(autoreset=True)

# Global Vars
OUTPUT_DIR = "configs"
CSV_DIR = "CSV"
JINJA_TEMPLATE = "switch.j2"
PARAMS_FILE = path.join(CSV_DIR, "01_params.csv")
VLANS_FILE = path.join(CSV_DIR, "02_vlans.csv")
ETHERCHANNELS_FILE = path.join(CSV_DIR, "03_etherchannels.csv")
PORT_MAPPING = path.join(CSV_DIR, "04_port_mapping.csv")
TODAY = str(date.today())


def build_template(
    template_file: str,
    parameters_file: str,
    vlans_file: str,
    etherchannels_file: str,
    port_mapping: str,
):
    """Generates a Cisco configuration template

    Args:
        template_file (str): path to switch.j2 file
        parameters_file (str): path to 01_parameters.csv file
        vlans_file (str): path 02_vlans.csv file
        etherchannels_file (str): path to 03_etherchannels.csv file
        port_mapping (str): path to 04_port-mapping.csv file
    """

    # Custom Jinja Filters
    def raise_helper(msg):
        raise SystemExit(cprint(msg, "red"))

    # Handle Jinja template
    env = Environment(
        loader=FileSystemLoader("./"), trim_blocks=True, lstrip_blocks=True
    )
    env.globals["raise"] = raise_helper

    template = env.get_template(JINJA_TEMPLATE)
    template.globals["now"] = datetime.now

    # Create configs directory if not created already
    if not path.exists(OUTPUT_DIR):
        mkdir(OUTPUT_DIR)

    # Read the "parameters" csv sheet and convert it to a dict
    with open(file=PARAMS_FILE, mode="r") as parameters:
        params = DictReader(parameters)
        for param in params:
            dict_params = dict(param)

    # Read the "vlans" csv sheet and convert it to a dict
    with open(file=VLANS_FILE, mode="r") as vlans:
        vlans = DictReader(vlans)
        dict_vlans = {"vlans": []}
        for vlan in vlans:
            dict_vlans["vlans"].append(dict(vlan))

    # Read the "etherchannels" csv sheet and convert it to a dict
    with open(file=ETHERCHANNELS_FILE, mode="r") as etherchannels:
        portchannels = DictReader(etherchannels)
        dict_portchannels = {"etherchannels": []}
        for portchannel in portchannels:
            dict_portchannels["etherchannels"].append(dict(portchannel))

    # Read the "port mapping" csv sheet and convert it to a dict
    with open(file=PORT_MAPPING, mode="r") as interfaces:
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

    # Create a json file for validation
    with open(file="json_schema.json", mode="w", encoding="utf-8") as outfile:
        json.dump(obj=dicts, fp=outfile, indent=4)

    # Validate Cisco Configuration
    cisco_validation = validate_cisco_config()
    if cisco_validation[0]:
        # Generate the configuration template file
        config = template.render(dicts)
        file_name = f"{dicts['hostname']}_{TODAY}"
        file_ext = "txt"
        file_location = path.join(OUTPUT_DIR, f"{file_name}.{file_ext}")
        with open(file=file_location, mode="w", encoding="utf-8") as cfg_file:
            cfg_file.write(config)

        cprint(
            f"Configuration file '{file_name}.{file_ext}' is created successfully!\n",
            "green",
        )
        # Open configuration file in the default Text Editor for the .txt file extension
        decision = (
            input(f"Do you want to open {file_name}.{file_ext} file now? [y/N]: ")
            or "N"
        )
        if decision in ("N", "n"):
            cprint(
                f"INFO: '{file_name}.{file_ext}' is created in configs directory.",
                "blue",
            )
        elif decision in ("Y", "y"):
            cprint(f"Opening '{file_name}.{file_ext}', please wait...", "cyan")
            sleep(1)
            TextEditor.open(file_location, new=0)
        else:
            raise SystemExit(cprint("Invalid input value!", "red"))
    else:
        cprint("Something went wrong. Please check the following errors.", "red")
        errors = cisco_validation[1]
        for key, value in errors.items():
            cprint(f"Error(s): {key}: {value}", "red")


if __name__ == "__main__":
    build_template(
        JINJA_TEMPLATE, PARAMS_FILE, VLANS_FILE, ETHERCHANNELS_FILE, PORT_MAPPING
    )
