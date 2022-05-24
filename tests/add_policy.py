#!/usr/bin/env python3
#
# Add a new policy
#

import json
import sys

from sdcclient import SdSecureClient
from sysdig_cfg import *

def usage():
    print(('usage: %s <policy-file>' % sys.argv[0]))
    print('Reads policy json from file')
    print('You can find your token at https://secure.sysdig.com/#/settings/user')
    sys.exit(1)


#
# Parse arguments
#
if len(sys.argv) != 2:
    usage()

policy_file_name = sys.argv[1]

f = open(policy_file_name, 'r')
policy_json = f.read()

#
# Instantiate the SDC client
#
sdclient = SdSecureClient(sysdig_api_token, 'https://' + sysdig_host)

ok, res = sdclient.add_policy_json(policy_json)

#
# Return the result
#
if ok:
    print((json.dumps(res, indent=2)))
else:
    print(res)
    sys.exit(1)
