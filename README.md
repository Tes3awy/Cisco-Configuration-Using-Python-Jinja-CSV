# Generate Cisco Configuration Template Using Python, Jinja2, and CSV

## Table of Contents

1. [Requirements](#1-requirements)
2. [How to Install Python Libraries?](#2-how-to-install-python-libraries)
3. [Getting Started](#3-getting-started)
4. [Usage](#4-usage)
5. [Preview](#5-preview)

### 1. Requirements

1. [Python @3.9.4](https://www.python.org/)
2. [Jinja2 @2.11.3](https://jinja.palletsprojects.com/en/2.11.x/)
3. [Visual Studio Code](https://code.visualstudio.com/) (Optional but recommended)
4. [Cisco IOS Syntax](https://marketplace.visualstudio.com/items?itemName=jamiewoodio.cisco) (Extension for Cisco IOS Syntax Highlighting)

---

### 2. How to install Python Libraries?

#### Jinja2

```python3
pip install jinja2 --user
```

---

### 3. Getting Started

In this repo, you can find four `.csv` files:

1. params.csv
2. vlans.csv
3. etherchannels.csv
4. port_mapping.csv

and

5. config_generator.py
6. switch.j2

> Ignore other files.

---

### 4. Usage

1. Open each `.csv` file _(respectively)_, and add the configurations that meet your needs. _(The files are populated already)_
2. Open Visual Studio Code.
3. Open Terminal within VSCode (`` Ctrl+` ``).
4. Run `py config_generator.py`

Voila :sparkles:! Your configuration will automagically open in default text editor.

All generated configuration files are stored in `configs` directory.

> If the `.ios` file extension is not associated with any text editor on your machine, please associate it with VSCode.

---

### 5. Preview

![Preview](preview.png)
