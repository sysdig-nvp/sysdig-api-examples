#!/usr/bin/env python3

#
# Get the sysdig secure user rules file.
#

import sys

sys.path.append('../')
from sysdig_cfg import *

from sdcclient import SdSecureClient

#
# Instantiate the SDC client
#
sdclient = SdSecureClient(sysdig_api_token, 'https://' + sysdig_host)

#
# Get the configuration
#
#ok, res = sdclient.get_user_falco_rules()
ok, res = sdclient.get_system_falco_rules()

#
# Return the result
#
if ok:
    #sys.stdout.write(res)
    print(res)
else:
    print(res)
    sys.exit(1)
