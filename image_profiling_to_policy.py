#!/usr/bin/env python3

import sys, time
import http.client
import urllib
import json
import pprint

from sysdig_cfg import *

DEBUG = 0

image_profiles = {}

start_num = time.time() - (86400 * 60)
end_num = time.time() + 86400

auth_header = "Bearer %s" % (sysdig_api_token)
content_type_header = "application/json;charset=UTF-8"

conn = http.client.HTTPSConnection(sysdig_host)

def httpRequest(inUri = None):
    conn.request("GET", inUri, None, {"Authorization": auth_header, "Content-Type": content_type_header})

    res = conn.getresponse()
    data = res.read()

    indata = data.decode("utf-8").strip()
    return json.loads(indata)

def getImageProfileGroups():
    theUri = '/api/v1/profiling/profileGroups'

    return httpRequest(theUri)

def getImageProfileIdsByGroup(jsonIn = None):
    image_profile_group_ids = []

    if 'ProfileGroups' in jsonIn:
        for profile_group in jsonIn['ProfileGroups']:
            image_profile_group_ids.append(profile_group['id'])
    return image_profile_group_ids

def getImageProfilesById(inId = []):
    image_uris_by_id = []

    for image_profile_id in inId:
        theUri = urllib.parse.quote("/api/v1/profiling/profileGroups/%s/profiles" % image_profile_id)
        print("uggg ", theUri)
        image_uris_by_id.append(theUri)
    return image_uris_by_id

def fooblah(inUris = []):
    for inUri in inUris:
       print("fooblah ", inUri)
       print("uhhh ", httpRequest(inUri))


image_profiles = getImageProfileGroups()

image_profile_group_ids = getImageProfileIdsByGroup(image_profiles)
print(image_profile_group_ids)

"""
{'name': 'UDP OUT Ports', 'ruleName': 'UDP OUT Ports - gcr.io/stackdriver-agents/metadata-agent-go:1.2.0@73dadc1c6bf4d57dc428933e7effc4049b17687b830cc2bb134fd12661afc003', 'ruleType': 'NETWORK', 'score': 0}], 'score': 0}, 'containerImagesProposal': {'subcategories': [{'name': 'Containers detected', 'ruleName': 'Containers detected - gcr.io/stackdriver-agents/metadata-agent-go:1.2.0@73dadc1c6bf4d57dc428933e7effc4049b17687b830cc2bb134fd12661afc003', 'ruleType': 'CONTAINER', 'score': 0}], 'score': 0}, 'status': 'LEARNING', 'score': 0}]}
"""
blahblah = getImageProfilesById(image_profile_group_ids)
fooblah(blahblah)

#print(topology_map)
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(json.dumps(topology_map))
