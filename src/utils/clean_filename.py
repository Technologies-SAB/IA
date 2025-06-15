import requests
import re
import os

def clean(name):
     name = re.sub(r'[<>:"/\\|?*\t]', '_', name)
     name = name.replace(';', '_')
     return name