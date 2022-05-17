#!/usr/bin/env python3

import sys, time
import http.client
import json

from sysdig_cfg import *

topology_map = {}
topology_map['clusters'] = []

start_num = time.time() - (86400 * 60)
end_num = time.time() + 86400

auth_header = "Bearer %s" % (sysdig_demo_api_token)
content_type_header = "application/json;charset=UTF-8"

conn = http.client.HTTPSConnection(sysdig_demo_host)

def httpRequest(inUri = None):
    conn.request("GET", inUri, None, {"Authorization": auth_header, "Content-Type": content_type_header})

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8").strip())

def getK8sClusters():
    theUri = '/api/v1/networkTopology/clusters?from=%d&to=%d' % (start_num, end_num)

    return httpRequest(theUri)

def getK8sNamespaces(inK8sClusterName = None):
    theUri = '/api/v1/networkTopology/namespaces?cluster=%s&from=%d&to=%d' % (inK8sClusterName, start_num, end_num)
    return httpRequest(theUri)

def getK8sAppOwners(inK8sClusterName = None, inK8sNamespaceName = None):
    theUri = '/api/v1/networkTopology/owners?cluster=%s&namespace=%s&from=%d&to=%d' % (inK8sClusterName, inK8sNamespaceName, start_num, end_num)
    return httpRequest(theUri)

def getIngressInfo(inK8sClusterName = None, inK8sNamespaceName = None, inName = None, inKind = None):
    theUri = '/api/v1/networkTopology/ingressSummaries?cluster=%s&namespace=%s&name=%s&kind=%s&from=%d&to=%d' % (inK8sClusterName, inK8sNamespaceName, inName, inKind, start_num, end_num)
    return httpRequest(theUri)

def getIngressUnusedInfo(inK8sClusterName = None, inK8sNamespaceName = None, inName = None, inKind = None):
    theUri = '/api/v1/networkTopology/ingressUnresolvedIps?cluster=%s&namespace=%s&name=%s&kind=%s&from=%d&to=%d' % (inK8sClusterName, inK8sNamespaceName, inName, inKind, start_num, end_num)
    return httpRequest(theUri)

def getEgressInfo(inK8sClusterName = None, inK8sNamespaceName = None, inName = None, inKind = None):
    theUri = '/api/v1/networkTopology/egressSummaries?cluster=%s&namespace=%s&name=%s&kind=%s&from=%d&to=%d' % (inK8sClusterName, inK8sNamespaceName, inName, inKind, start_num, end_num)
    return httpRequest(theUri)

def getEgressUnusedInfo(inK8sClusterName = None, inK8sNamespaceName = None, inName = None, inKind = None):
    theUri = '/api/v1/networkTopology/egressUnresolvedIps?cluster=%s&namespace=%s&name=%s&kind=%s&from=%d&to=%d' % (inK8sClusterName, inK8sNamespaceName, inName, inKind, start_num, end_num)
    return httpRequest(theUri)

k8s_clusters = getK8sClusters()

for k8s_cluster in k8s_clusters:
    if k8s_cluster == '(not provided)' or k8s_cluster != 'demo-kube-aws':
        continue

    temp_h = {}
    if not k8s_cluster in temp_h:
        temp_h[k8s_cluster] = {}

    # Collect namespaces
    k8s_namespaces = getK8sNamespaces(k8s_cluster)

    for k8s_namespace in k8s_namespaces:
        if k8s_namespace['name'] != 'example-java-app':
            continue

        print(k8s_namespace['name'])
        temp_h[k8s_cluster][k8s_namespace['name']] = {}
        k8s_app_owners = getK8sAppOwners(k8s_cluster, k8s_namespace['name'])

        for k8s_app_owner in k8s_app_owners:
            ingress_data = getIngressInfo(k8s_cluster, k8s_namespace['name'], k8s_app_owner['name'], k8s_app_owner['kind'])
            if len(ingress_data['connections']) > 0:
                print("ingress ---> ", ingress_data)

            print("ingress unused ---> ", getIngressUnusedInfo(k8s_cluster, k8s_namespace['name'], k8s_app_owner['name'], k8s_app_owner['kind']))
            print("\n\n")

            egress_data = getEgressInfo(k8s_cluster, k8s_namespace['name'], k8s_app_owner['name'], k8s_app_owner['kind'])
            if len(egress_data['connections']) > 0:
                print("ingress ---> ", egress_data)

            print("egress unused ---> ", getEgressUnusedInfo(k8s_cluster, k8s_namespace['name'], k8s_app_owner['name'], k8s_app_owner['kind']))
            print("\n\n\n\n")

    print(temp_h)
