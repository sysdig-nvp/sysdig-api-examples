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

def getImageProfileGroupIds():
    theUri = '/api/v1/profiling/profileGroups'

    return httpRequest(theUri)

def getImageProfileIdsByGroupId(jsonIn = None):
    image_profile_group_ids = []

    if 'ProfileGroups' in jsonIn:
        for profile_group in jsonIn['ProfileGroups']:
            image_profile_group_ids.append(profile_group['id'])
    return image_profile_group_ids

def getImageProfilesByGroupId(inId = []):
    image_uris_by_id = []

    for image_profile_id in inId:
        theUri = urllib.parse.quote("/api/v1/profiling/profileGroups/%s/profiles" % image_profile_id)
        image_uris_by_id.append(theUri)
    return image_uris_by_id

def getImageProfiles(inUris = []):
    for inUri in inUris:
       return httpRequest(inUri)

def getImageProfileByProfileId(inProfile = {}):
    inUri = "/api/v1/profiling/profiles/%s" % inProfile['profileId']

    #
    # Don't attempt to create policy for any image that we are
    # still learning about
    #
    if inProfile['status'] != 'LEARNING':
#        print(inProfile)
#        print(inUri)
#        print("\n")
        return httpRequest(inUri)
    return None

image_profile_group_ids = getImageProfileGroupIds()
image_profile_group_ids = getImageProfileIdsByGroupId(image_profile_group_ids)

"""
{'name': 'UDP OUT Ports', 'ruleName': 'UDP OUT Ports - gcr.io/stackdriver-agents/metadata-agent-go:1.2.0@73dadc1c6bf4d57dc428933e7effc4049b17687b830cc2bb134fd12661afc003', 'ruleType': 'NETWORK', 'score': 0}], 'score': 0}, 'containerImagesProposal': {'subcategories': [{'name': 'Containers detected', 'ruleName': 'Containers detected - gcr.io/stackdriver-agents/metadata-agent-go:1.2.0@73dadc1c6bf4d57dc428933e7effc4049b17687b830cc2bb134fd12661afc003', 'ruleType': 'CONTAINER', 'score': 0}], 'score': 0}, 'status': 'LEARNING', 'score': 0}]}
"""
image_profiles_by_group_id = getImageProfilesByGroupId(image_profile_group_ids)
all_image_profiles = getImageProfiles(image_profiles_by_group_id)

# dict_keys(['offset', 'limit', 'canLoadMore', 'profiles'])
#print(all_image_profiles.keys())

for image_profile in all_image_profiles['profiles']:
    generated_image_profile = getImageProfileByProfileId(image_profile)
    if generated_image_profile != None:
        print(generated_image_profile)

#print(topology_map)
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(json.dumps(topology_map))
