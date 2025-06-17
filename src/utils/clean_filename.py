import requests
import re
import os

def clean(name):
     name = re.sub(r'[<>:"/\\|?*\t]', '_', name)
     name = name.replace(';', '_')
     return name

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", filename)