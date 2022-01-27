#!/usr/bin/python3

import requests

r = requests.get('http://product:8000/api/deploy')
print(r)
