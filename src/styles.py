"""This module contains the primary text styles for this application.

This module uses the colored package and is used to set variables for common text styling combinations for use in main.py and functions.py
"""

import colored

blue_bold = colored.fg("#68b5ff") + colored.attr("bold")
blue = colored.fg("#68b5ff")
red_bold = colored.fg("red") + colored.attr("bold")
bold = colored.attr("bold")