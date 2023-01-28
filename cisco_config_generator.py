#!/usr/bin/env python3

# ---------------------------------------------------------------------------------------
#
# Demonstrates how to generate Cisco configuration template using Python3, Jinja2 and CSV
#
# (C) 2021 Osama Abbas, Cairo, Egypt
# Released under MIT License
#
# Filename: cisco_config_generator.py
# Version: Python 3.11.1
# Authors: Osama Abbas (oabbas2512@gmail.com)
# Description:   This program is designed to generate a configuration template
#                for Cisco Catalyst/Nexus switches.
#
# ---------------------------------------------------------------------------------------

# Libraries
import json
import os
import time
import webbrowser as TextEditor
from csv import DictReader
from datetime import date, datetime

from colorama import init
from jinja2 import Environment, FileSystemLoader
from termcolor import cprint

from validate_config import validate_config

init(autoreset=True)

# Global Vars
CSV_DIR = "CSV"
JINJA_TEMPLATE = "switch.j2"
PARAMS_FILE = os.path.join(CSV_DIR, "01_params.csv")
VLANS_FILE = os.path.join(CSV_DIR, "02_vlans.csv")
ETHERCHANNELS_FILE = os.path.join(CSV_DIR, "03_etherchannels.csv")
PORT_MAPPING = os.path.join(CSV_DIR, "04_port_mapping.csv")
OUTPUT_DIR = "configs"


def build_template(
    template_file: str = JINJA_TEMPLATE,
    parameters_file: str = PARAMS_FILE,
    vlans_file: str = VLANS_FILE,
    etherchannels_file: str = ETHERCHANNELS_FILE,
    port_mapping: str = PORT_MAPPING
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
    def raise_helper(msg: str):
        raise SystemExit(cprint(msg, "red"))

    # Handle Jinja template
    env = Environment(
        loader=FileSystemLoader("./"), trim_blocks=True, lstrip_blocks=True
    )
    env.globals["raise"] = raise_helper
    template = env.get_template(name=template_file)
    template.globals["now"] = datetime.now().replace(microsecond=0)

    # Create configs directory if not created already
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    # Read the "parameters" csv sheet and convert it to a dict
    with open(file=parameters_file, mode="rt", encoding="utf-8") as params:
        for param in DictReader(params):
            dict_params = dict(param)

    # Read the "vlans" csv sheet and convert it to a dict
    with open(file=vlans_file, mode="rt", encoding="utf-8") as vlans:
        dict_vlans = {"vlans": []}
        for vlan in DictReader(vlans):
            dict_vlans["vlans"].append(dict(vlan))

    # Read the "etherchannels" csv sheet and convert it to a dict
    with open(file=etherchannels_file, mode="rt", encoding="utf-8") as etherchannels:
        portchannels = DictReader(etherchannels)
        dict_portchannels = {"etherchannels": []}
        for portchannel in portchannels:
            dict_portchannels["etherchannels"].append(dict(portchannel))

    # Read the "port mapping" csv sheet and convert it to a dict
    with open(file=port_mapping, mode="rt", encoding="utf-8") as interfaces:
        dict_ports = {"interfaces": []}
        for port in DictReader(interfaces):
            dict_ports["interfaces"].append(dict(port))

    # Combine all four csv sheets
    dict_params.update(dict_vlans)
    dict_params.update(dict_portchannels)
    dict_params.update(dict_ports)

    # Create a json file for validation
    with open(file="json_schema.json", mode="wt", encoding="utf-8") as schema_file:
        json.dump(obj=dict_params, fp=schema_file, indent=4)

    # Validate Cisco Configuration
    validation = validate_config(schema=schema_file.name)
    if validation.get("is_validated"):
        # Generate the configuration template file
        config = template.render(dict_params)
        file_name = f"{dict_params.get('hostname')}_{date.today()}"
        file_ext = "txt"
        file_path = os.path.join(OUTPUT_DIR, f"{file_name}.{file_ext}")
        with open(file=file_path, mode="wt", encoding="utf-8") as cfg_file:
            cfg_file.write(config)

        cprint(
            f"Configuration file '{file_name}.{file_ext}' is created!",
            "green",
            end="\n\n"
        )
        # Open configuration file in the default Text Editor for the .txt file extension
        decision = (
            input(f"Do you want to open {file_name}.{file_ext} file now? [y/N]: ")
            or "n"
        ).lower()
        if decision == "n":
            cprint(
                f"INFO: '{file_name}.{file_ext}' is created in configs directory.",
                "blue",
            )
        elif decision == "y":
            cprint(f"Opening '{file_name}.{file_ext}', please wait...", "cyan")
            time.sleep(1)
            TextEditor.open(file_path, new=0)
        else:
            raise SystemExit(cprint("Skipped", "yellow"))
    else:
        cprint("Something went wrong! Check the following errors.", "red")
        errors = validation.get("errors")
        for k, val in errors.items():
            cprint(f"Errors: {k}: {val}", "red")


if __name__ == "__main__":
    build_template()
