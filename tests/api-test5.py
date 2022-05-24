#!/usr/bin/env python3

#
# Get alert notifications from Sysdig Cloud
#

import sys
import time

from sdcclient import SdcClient
from sysdig_cfg import *

time_factor = 86400

def print_notifications(notifications):
    for notification in notifications:
        values = []
        for entity in notification['entities']:
            for value in entity['metricValues']:
                values.append(str(value['value']))
        notification.update({'values': ','.join(values)})
        notification["filter"] = notification.get("filter", "")
        print("#%(id)s, State: %(state)s, Severity: %(severity)s, Scope: %(filter)s, Condition: %(condition)s, "
              "Value: %(values)s, Resolved: %(resolved)s" %
              notification)


sdc_token = sysdig_api_token
sysdig_url = 'https://' + sysdig_host

#
# Instantiate the SDC client
#
sdclient = SdcClient(sdc_token, sysdig_url)

#
# Get the notifications in the last day
#
ok, res = sdclient.get_notifications(
    from_ts=int(time.time() - time_factor),
    to_ts=int(time.time()))

print_notifications(res['notifications'])
if not ok:
    sys.exit(1)

#
# Get the notifications in the last day and active state
#
ok, res = sdclient.get_notifications(
    from_ts=int(time.time() - time_factor),
    to_ts=int(time.time()), state='ACTIVE')

print_notifications(res['notifications'])
if not ok:
    sys.exit(1)

#
# Get the notifications in the last day and active state
#
ok, res = sdclient.get_notifications(
    from_ts=int(time.time() - time_factor),
    to_ts=int(time.time()), state='OK')

print_notifications(res['notifications'])
if not ok:
    sys.exit(1)

#
# Get the notifications in the last day and resolved state
#
ok, res = sdclient.get_notifications(
    from_ts=int(time.time() - time_factor),
    to_ts=int(time.time()),
    resolved=True)

print_notifications(res['notifications'])
if not ok:
    sys.exit(1)
