#!/usr/bin/env python3

import time
import http.client
import json

from sysdig_cfg import *

topology_map = {}
topology_map['clusters'] = []

conn = http.client.HTTPSConnection(sysdig_demo_host)

start_num = time.time() - (86400 * 60)
end_num = time.time() + 86400

auth_header = "Bearer %s" % (sysdig_demo_api_token)
content_type_header = "application/json;charset=UTF-8"

conn.request("GET", "/api/v1/networkTopology/clusters?from=%d&to=%d" % (start_num, end_num), None, {"Authorization": auth_header, "Content-Type": content_type_header})

res = conn.getresponse()
data = res.read()

#print(data.decode("utf-8").strip())
#print(type(data.decode("utf-8")))

raw_k8s_clusters_output = data.decode("utf-8").strip()
k8s_clusters = json.loads(raw_k8s_clusters_output)
print (k8s_clusters)

for k8s_cluster in k8s_clusters:
    if k8s_cluster == '(not provided)' or k8s_cluster != 'demo-kube-aws':
        continue

    print(k8s_cluster)

    temp_h = {}
    if not k8s_cluster in temp_h:
        temp_h[k8s_cluster] = {}
        temp_h[k8s_cluster]['namespaces'] = []

    # Collect namespaces
    conn.request("GET", "/api/v1/networkTopology/namespaces?cluster=%s&from=%d&to=%d" % (k8s_cluster, start_num, end_num), None, {"Authorization": auth_header, "Content-Type": content_type_header})
    res = conn.getresponse()
    data = res.read()

    #print(data.decode("utf-8").strip())
    #print(type(data.decode("utf-8")))
    k8s_namespaces = json.loads(data.decode("utf-8").strip())
    print(k8s_namespaces)

    for k8s_namespace in k8s_namespaces:
        print(k8s_namespace['name'])
#        temp_h[k8s_cluster]['namespaces'] = []

    print(temp_h)
