#!/usr/bin/env python3

import os
import json
import requests

from sysdig_cfg import *

print(dir())

f = open(swagger_json)

swagger = json.load(f)
print(swagger)
print(swagger['openapi'])
print(swagger.keys())
print(swagger['paths'].keys())
