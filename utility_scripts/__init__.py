#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""Utility scripts package. This package contains useful utility scripts separated into modules by functionality.

.env support:
    To utilize .env files for loading environment variables, if .env is in the working directory run:

    from dotenv import load_dotenv
    load_dotenv()

    optionally specifying a path to the .env file using:
    load_dotenv(dotenv_path='path/to/.env')

Modules:

    dash_tools.py
        - Objects assocaiated with Dash app development.

    dbase.py
        - Objects associated with database connections.

    email.py
        - Objects associated with email functionality.

    fsconn.py
        - Objects associated with fileserver connections.

    log.py
        - Objects associated with application logging.
"""

# import all needed objects
# usage: import utility_scripts as us
# then call objects as us.Mail() etc.

# import all dash_tools, dbase, fsconn, and log
from .dash_tools import *
from .dbase import *
from .fsconn import *
from .log import *

# only import the Mail class from email
from .email import Mail


# also allow each module to be import explicitly
# usage: from utility_scripts import email
import utility_scripts.dash_tools
import utility_scripts.dbase
import utility_scripts.email
import utility_scripts.fsconn
import utility_scripts.log
