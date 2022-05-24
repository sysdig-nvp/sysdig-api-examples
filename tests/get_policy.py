#!/usr/bin/env python3
#
# Get a specific policy
#

import json
import sys

from sdcclient import SdSecureClient
from sysdig_cfg import *

def usage():
    print(('usage: %s <policy name>' % sys.argv[0]))
    print('You can find your token at https://secure.sysdig.com/#/settings/user')
    sys.exit(1)


#
# Parse arguments
#
if len(sys.argv) != 2:
    usage()

name = sys.argv[1]

#
# Instantiate the SDC client
#
sdclient = SdSecureClient(sysdig_api_token, 'https://' + sysdig_host)

ok, res = sdclient.get_policy(name)

#
# Return the result
#
if ok:
    print((json.dumps(res, indent=2)))
else:
    print(res)
    sys.exit(1)
