#!/usr/bin/env python

# ------------------------------------------------------------------------
#
# Demonstrates how to validate Cisco configuration
#
# (C) 2021 Osama Abbas, Cairo, Egypt
# Released under MIT License
#
# Filename: cisco_validation.py
# Version: Python 3.9.4
# Authors: Osama Abbas (oabbas2512@gmail.com)
# Description:   This program is designed to validate Cisco configuration
#
# ------------------------------------------------------------------------

import ipaddress
import json

from cerberus import Validator

json_schema = {
    "hostname": {
        "type": "string",
        "minlength": 1,
        "maxlength": 63,
        "required": True,
        "empty": False,
        "regex": "[A-Za-z0-9_-]+",
    },
    "timezone": {"type": "string", "required": True, "empty": False},
    "domain_name": {
        "type": "string",
        "required": True,
        "empty": False,
        "regex": "[/^\S+$/]+",
    },
    "stp_mode": {
        "type": "string",
        "required": True,
        "empty": False,
        "allowed": ["pvst", "rapid-pvst", "mst"],
    },
    "vtp_domain": {"type": "string", "required": False, "empty": True},
    "vtp_version": {"type": "string", "required": False, "allowed": ["1", "2", "3"]},
    "vtp_mode": {
        "type": "string",
        "required": True,
        "empty": False,
        "allowed": ["client", "server", "transparent", "off"],
    },
    "logging_console": {"type": "string", "required": False, "empty": True},
    "logging_buffer_size": {"type": "string"},
    "http_server": {
        "type": "string",
        "required": False,
        "empty": True,
        "allowed": ["yes", "no"],
    },
    "errdisable": {
        "type": "string",
        "required": False,
        "empty": True,
        "allowed": ["yes", "no"],
    },
    "errdisable_recovery_interval": {
        "type": "string",
        "required": False,
        "empty": True,
        "dependencies": ["errdisable"],
        "regex": "[0-9]+",
    },
    "lldp": {
        "type": "string",
        "required": False,
        "empty": True,
        "allowed": ["yes", "no"],
    },
    "username": {"type": "string", "required": True, "empty": False},
    "algorithm_type": {
        "type": "string",
        "required": True,
        "empty": False,
        "allowed": ["scrypt", "sha256"],
    },
    "password": {"type": "string", "required": True, "empty": False},
    "enable_password": {"type": "string", "required": False, "empty": True},
    "ssh_key_size": {
        "type": "string",
        "required": False,
        "empty": True,
        "regex": "[0-9]+",
    },
    "ssh_version": {
        "type": "string",
        "required": False,
        "empty": True,
        "regex": "[0-9]+",
    },
    "vty_lines": {
        "type": "string",
        "required": False,
        "empty": True,
        "regex": "[0-9]+",
    },
    "login_local": {
        "type": "string",
        "required": False,
        "empty": True,
        "allowed": ["yes", "no"],
    },
    "timeout": {"type": "string", "required": False, "empty": True, "regex": "[0-9]+"},
    "transport_input": {
        "type": "string",
        "required": False,
        "empty": True,
        "allowed": ["ssh", "telnet", "all"],
    },
    "transport_output": {
        "type": "string",
        "required": False,
        "empty": True,
        "allowed": ["ssh", "telnet", "all"],
    },
    "vlans": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "id": {"type": "string", "required": True, "regex": "[0-9]+"},
                "name": {"type": "string", "required": True},
                "ip_addr": {"type": "string", "required": False},
                "mask": {"type": "string", "required": False},
                "desc": {"type": "string", "required": False},
            },
        },
    },
    "etherchannels": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "id": {"type": "string", "required": True, "regex": "[0-9]+"},
                "type": {
                    "type": "string",
                    "required": True,
                    "empty": False,
                    "allowed": ["L2", "l2", "L3", "l3"],
                },
                "mode": {"type": "string", "required": False, "empty": True},
                "access_vlan": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                    "regex": "[0-9]+",
                },
                "native_vlan": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                    "regex": "[0-9]+",
                },
                "allowed_vlans": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                },
                "ip_addr": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                },
                "mask": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                },
                "desc": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                },
            },
        },
    },
    "interfaces": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {
                    "type": "string",
                    "required": True,
                    "empty": False,
                    "regex": "[\D+\d+((/\d+)+(\.\d+)?)?]+",
                },
                "mode": {
                    "type": "string",
                    "required": True,
                    "empty": False,
                },
                "access_vlan": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                    "regex": "[0-9]+",
                },
                "voice_vlan": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                    "regex": "[0-9]+",
                },
                "native_vlan": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                    "regex": "[0-9]+",
                },
                "allowed_vlans": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                },
                "portfast": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                    "allowed": ["yes", "no"],
                },
                "bpduguard": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                    "allowed": ["yes", "no"],
                },
                "portsecurity": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                    "allowed": ["yes", "no"],
                },
                "description": {"type": "string", "required": False, "empty": True},
            },
        },
    },
}


def validate_cisco_config() -> list[bool, dict]:
    v = Validator()
    with open("json_schema.json", "r") as f:
        document = json.load(f)

    return [v.validate(document, json_schema), v.errors]
