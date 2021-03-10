from pathlib import Path
from typing import Tuple
import asyncio
import discord
import json
import os
import requests

'''
SETUP:
Go to line 19 and replace Details.json with your JSON file's name.

Then load your functions in your python file and enjoy! (Example of grabbing data below)
'''

def load_config() -> Tuple[dict, Path]:
    """Load data from the botconfig.json.\n
    Returns a tuple containing the data as a dict, and the file as a Path"""
    config_file = Path("Details.json"). # REPLACE THIS WITH YOUR JSON FILE
    config_file.touch(exist_ok=True)
    if config_file.read_text() == "":
        config_file.write_text("{}")
    with config_file.open("r") as f:
        config = json.load(f)
    return config, config_file

def prompt_config(msg, key):
    """Ensure a value exists in the botconfig.json, if it doesn't prompt the bot owner to input via the console."""
    config, config_file = load_config()
    if key not in config:
        config[key] = msg
        with config_file.open("w+") as f:
            json.dump(config, f, indent=4)
            
            
#USAGE EXAMPLE:

from file import prompt_config, load_config #replace file here with file name
config, _ = load_config()

print(f"Hey there! My syntax is {config["Syntax"]}") #This grabs the "Syntax" field in your JSON file. 
