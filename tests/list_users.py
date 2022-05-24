#!/usr/bin/env python3

#
# List all the users in a Sysdig Monitor environment. The token you provide must
# have Admin rights.
#

import sys

from sdcclient import SdcClient
from sysdig_cfg import *

sdc_token = sysdig_demo_api_token

#
# Instantiate the SDC client
#
sdclient = SdcClient(sdc_token, 'https://app.sysdigcloud.com')

#
# Get the configuration
#
ok, res = sdclient.get_users()
if ok:
    print('Users\n=====')
    for user in res:
        print((user['username']))
else:
    print(res)
    sys.exit(1)
