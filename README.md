[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/Tes3awy/Cisco-Configuration-Using-Python-Jinja-CSV)
[![Tested on Python 3.11.1](https://img.shields.io/badge/Tested%20-Python%203.11.1-blue.svg?logo=python)](https://www.python.org/downloads)
[![Contributions Welcome](https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3)]()
[![License](https://img.shields.io/github/license/Tes3awy/Cisco-Configuration-Using-Python-Jinja-CSV)](hhttps://github.com/Tes3awy/Cisco-Configuration-Using-Python-Jinja-CSV)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Generate Cisco Configuration Template Using Python3, Jinja2, and CSV with Validation

This program is designed to generate a configuration template for Cisco Catalyst/Nexus switches.

## Table of Contents

1. [Requirements](#requirements)
2. [Getting Started](#getting-started)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Preview](#preview)
6. [Helpful Tips](#helpful-tips)
7. [TODOs](#todos)

---

### Requirements

1. [Python @3.11.1](https://www.python.org/)
2. [Jinja2 @3.1.2](https://jinja.palletsprojects.com/en/3.1.x/)

### Getting Started

```bash
│   cisco_config_generator.py
│   cisco_validation.py
│   switch.j2
│   requirements.txt
│   README.md
│   .gitignore
│   LICENSE
│
├───assets
│       preview.png
│
├───configs
│       .gitkeep
│
└───CSV
        01_params.csv
        02_vlans.csv
        03_etherchannels.csv
        04_port_mapping.csv

```

### Installation

```bash
$ git clone https://github.com/Tes3awy/Cisco-Configuration-Using-Python-Jinja-CSV.git
$ cd Cisco-Configuration-Using-Python-Jinja-CSV
$ python -m venv .venv --upgrade-deps
# Activate Virtual Environment
$ pip install -r requirements.txt
```

### Usage

1. Open each `.csv` file _respectively_ and add the configurations that meet your needs. _(The CSV files are populated with a sample configuration already)_
2. Open terminal/cmd.
3. Run `python cisco_config_generator.py`.

First, a `json_schema.json` file is created _(if not created already)_ from your configuration in CSV files. Then, `json_schema.json` is validated against a set of rules in `validate_config.py`.

Voila :sparkles:! Your configuration will be created an placed in configs directory.

### Preview

![Preview](assets/preview.png)

### Helpful Tips

1. **DO NOT** copy/paste the whole configuration all at once to your device. Divide the configuration template into multiple sections.
2. Always save your configuration with the `copy running-config startup-config` command. [See Why](https://networkengineering.stackexchange.com/questions/52309/diffrence-between-wr-and-copy-running-config-to-startup-config#answer-52310)

### TODOs

- [x] ~~Validate input fields in CSV files~~.
