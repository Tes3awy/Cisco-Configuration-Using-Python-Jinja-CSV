import os
import json
import ipaddress
from cerberus import Validator

json_schema = {
    "hostname": {
        "type": "string",
        "maxlength": 63,
        "minlength": 1,
        "required": True,
        "empty": False,
        "regex": "[A-Za-z0-9_-]+",
    },
    "timezone": {"type": "string", "required": True, "empty": False},
    "domain_name": {"type": "string", "required": False, "empty": True},
    "stp_mode": {"type": "string", "required": True, "empty": False},
    "vtp_domain": {"type": "string", "required": False, "empty": True},
    "vtp_version": {"type": "string", "required": False},
    "vtp_mode": {"type": "string", "required": True, "empty": False},
    "logging_console": {"type": "string", "required": False, "empty": True},
    "logging_buffer_size": {"type": "string"},
    "http_server": {"type": "string", "required": False, "empty": True},
    "errdisable": {"type": "string", "required": False, "empty": True},
    "errdisable_recovery_interval": {
        "type": "string",
        "required": False,
    },
    "lldp": {"type": "string", "required": False, "empty": True},
    "username": {"type": "string", "required": True, "empty": False},
    "algorithm_type": {"type": "string", "required": True, "empty": False},
    "password": {"type": "string", "required": True, "empty": False},
    "enable_password": {"type": "string", "required": False, "empty": True},
    "ssh_key_size": {"type": "string", "required": False},
    "ssh_version": {"type": "string", "required": False},
    "vty_lines": {"type": ["string", "integer"], "required": False, "empty": True},
    "login_local": {
        "type": ["string", "integer"],
        "required": False,
        "empty": True,
    },
    "timeout": {"type": "string", "required": False},
    "transport_input": {"type": "string", "required": False, "empty": True},
    "transport_output": {"type": "string", "required": False, "empty": True},
    "vlans": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "id": {"type": "string", "min": 1, "max": 4094, "required": True},
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
                "id": {"type": "string", "required": True},
                "type": {"type": "string", "required": True, "empty": False},
                "mode": {"type": "string", "required": False, "empty": True},
                "access_vlan": {
                    "type": ["string", "integer"],
                    "required": False,
                    "empty": True,
                },
                "native_vlan": {
                    "type": ["string", "integer"],
                    "required": False,
                    "empty": True,
                },
                "allowed_vlans": {
                    "type": ["string", "integer"],
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
                "name": {"type": "string", "required": True, "empty": False},
                "mode": {"type": "string", "required": True, "empty": False},
                "access_vlan": {
                    "type": ["string", "integer"],
                    "required": False,
                    "empty": True,
                },
                "voice_vlan": {
                    "type": ["string", "integer"],
                    "required": False,
                    "empty": True,
                },
                "native_vlan": {
                    "type": ["string", "integer"],
                    "required": False,
                    "empty": True,
                },
                "allowed_vlans": {
                    "type": ["string", "integer"],
                    "required": False,
                    "empty": True,
                },
                "portfast": {"type": "string", "required": False, "empty": True},
                "bpduguard": {"type": "string", "required": False, "empty": True},
                "portsecurity": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                },
                "description": {"type": "string", "required": False, "empty": True},
            },
        },
    },
}


def validate_cisco_config():
    v = Validator()
    with open("json_schema.json", "r") as f:
        document = json.load(f)
    if v.validate(document, json_schema):
        return True
    else:
        return v.errors
