# Generate Cisco Configuration Template Using Python, Jinja2, and CSV

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Getting Started](#2-getting-started)
3. [How it Works?](#3-how-it-works)
4. [Preview](#4-preview)

### 1. Prerequisites

1. [Python @3.9.4](https://www.python.org/)
2. [Jinja2 @2.11.3](https://jinja.palletsprojects.com/en/2.11.x/)
3. [CSV @1.0](https://docs.python.org/3/library/csv.html)
4. [Visual Studio Code](https://code.visualstudio.com/) (Optional but recommended)
5. [Cisco IOS Syntax](https://marketplace.visualstudio.com/items?itemName=jamiewoodio.cisco) (Extension for Cisco IOS Syntax Highlighting)

---

### 2. Getting Started

In this repo, you can find four `.csv` files:

1. params.csv
2. vlans.csv
3. etherchannels.csv
4. port_mapping.csv

and

1. config_generator.py
2. switch.j2

---

### 3. How it Works?

1. Open each `.csv` file _(respectively)_, and add the configurations that meet your needs. _(The files are populated already)_
2. Open Visual Studio Code.
3. Open Terminal within VSCode (`` Ctrl+` ``).
4. Run `py config_generator.py`

Voila :sparkles:! Your configuration will automagically open in your default text editor.

> If the `.ios` file extension is not associated with any text editor on your machine, please associate it with VSCode.

---

### 4. Preview

![Preview](preview.png)
