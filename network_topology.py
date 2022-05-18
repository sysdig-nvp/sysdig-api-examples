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
            """
ingress --->  {'connections': [{'clientOwner': {'name': 'example-java-app-javaapp', 'labels': ['app.kubernetes.io/instance=example-java-app', 'app.kubernetes.io/name=example-java-app-javaapp'], 'excludedLabels': [], 'kind': 'Deployment', 'cluster': 'demo-kube-aws', 'namespace': 'example-java-app', 'podControllerLabels': None}, 'clientNamespace': {'name': 'example-java-app', 'labels': ['heritage=Helm', 'release=namespaces', 'app=raw', 'chart=raw-0.2.5'], 'excludedLabels': [], 'kind': 'Namespace', 'cluster': 'demo-kube-aws'}, 'serverProcess': 'java', 'serverPort': 9042, 'rowId': 'ir_example-java-app_Deployment_example-java-app-javaapp_9042'}, {'clientOwner': {'name': 'example-java-app-javaapp', 'labels': ['app.kubernetes.io/instance=example-java-app', 'app.kubernetes.io/name=example-java-app-javaapp'], 'excludedLabels': [], 'kind': 'Deployment', 'cluster': 'demo-kube-aws', 'namespace': 'example-java-app', 'podControllerLabels': None}, 'clientNamespace': {'name': 'example-java-app', 'labels': ['heritage=Helm', 'release=namespaces', 'app=raw', 'chart=raw-0.2.5'], 'excludedLabels': [], 'kind': 'Namespace', 'cluster': 'demo-kube-aws'}, 'serverProcess': 'kube-dns', 'serverPort': 9042, 'rowId': 'ir_example-java-app_Deployment_example-java-app-javaapp_9042'}, {'clientOwner': {'name': 'example-java-app-javaapp', 'labels': ['app.kubernetes.io/instance=example-java-app', 'app.kubernetes.io/name=example-java-app-javaapp'], 'excludedLabels': [], 'kind': 'Deployment', 'cluster': 'demo-kube-aws', 'namespace': 'example-java-app', 'podControllerLabels': None}, 'clientNamespace': {'name': 'example-java-app', 'labels': ['heritage=Helm', 'release=namespaces', 'app=raw', 'chart=raw-0.2.5'], 'excludedLabels': [], 'kind': 'Namespace', 'cluster': 'demo-kube-aws'}, 'serverProcess': 'dnsmasq', 'serverPort': 9042, 'rowId': 'ir_example-java-app_Deployment_example-java-app-javaapp_9042'}], 'metadata': {'resolvedFrom': 1647625581, 'resolvedTo': 1652895981}}
            """
            ingress_data = getIngressInfo(k8s_cluster, k8s_namespace['name'], k8s_app_owner['name'], k8s_app_owner['kind'])
            if len(ingress_data['connections']) > 0:
                print("ingress ---> ", ingress_data)
                for ig_conn in ingress_data['connections']:
                    print(ig_conn['clientOwner']['name'])
                    print(ig_conn['serverProcess'])
                    print(ig_conn['serverPort'])

                """
ingress unused --->  {'clusterSubnetsComplete': True, 'unresolveds': [{'clientIPMetadata': {'origin': 'external,external,external', 'ip': '100.127.107.174,100.127.107.174,100.127.107.174'}, 'serverProcess': 'java,kube-dns,dnsmasq', 'serverPort': {'port': 9042, 'protocol': 'TCP'}, 'alias': '', 'rowId': 'iu_external_100.127.107.174_9042'}, {'clientIPMetadata': {'origin': 'external,external', 'ip': '100.127.148.222,100.127.148.222'}, 'serverProcess': 'java,kube-dns', 'serverPort': {'port': 9042, 'protocol': 'TCP'}, 'alias': '', 'rowId': 'iu_external_100.127.148.222_9042'}]}
                """
            ingress_unused_data = getIngressUnusedInfo(k8s_cluster, k8s_namespace['name'], k8s_app_owner['name'], k8s_app_owner['kind'])
            if len(ingress_unused_data['unresolveds']) > 0:
              print("ingress unused ---> ", ingress_unused_data)

            print("\n\n")

            """
EGD  {'connections': [{'serverOwner': {'name': 'example-java-app-javaapp', 'labels': ['app.kubernetes.io/instance=example-java-app', 'app.kubernetes.io/name=example-java-app-javaapp'], 'excludedLabels': [], 'kind': 'Deployment', 'cluster': 'demo-kube-aws', 'namespace': 'example-java-app', 'podControllerLabels': None}, 'serverNamespace': {'name': 'example-java-app', 'labels': ['chart=raw-0.2.5', 'heritage=Helm', 'release=namespaces', 'app=raw'], 'excludedLabels': [], 'kind': 'Namespace', 'cluster': 'demo-kube-aws'}, 'clientProcess': 'cut', 'serverPort': 8080, 'rowId': 'er_example-java-app_Deployment_example-java-app-javaapp_8080'}], 'metadata': {'resolvedFrom': 1647692446, 'resolvedTo': 1652962846}}
ingress --->  {'connections': [{'serverOwner': {'name': 'example-java-app-javaapp', 'labels': ['app.kubernetes.io/instance=example-java-app', 'app.kubernetes.io/name=example-java-app-javaapp'], 'excludedLabels': [], 'kind': 'Deployment', 'cluster': 'demo-kube-aws', 'namespace': 'example-java-app', 'podControllerLabels': None}, 'serverNamespace': {'name': 'example-java-app', 'labels': ['chart=raw-0.2.5', 'heritage=Helm', 'release=namespaces', 'app=raw'], 'excludedLabels': [], 'kind': 'Namespace', 'cluster': 'demo-kube-aws'}, 'clientProcess': 'cut', 'serverPort': 8080, 'rowId': 'er_example-java-app_Deployment_example-java-app-javaapp_8080'}], 'metadata': {'resolvedFrom': 1647692446, 'resolvedTo': 1652962846}}
            """
            egress_data = getEgressInfo(k8s_cluster, k8s_namespace['name'], k8s_app_owner['name'], k8s_app_owner['kind'])
            if len(egress_data['connections']) > 0:
                print("egress ---> ", egress_data)

                for eg_conn in egress_data['connections']:
                    print(eg_conn['serverOwner']['name'])
                    print(eg_conn['clientProcess'])
                    print(eg_conn['serverPort'])

                """
egress unused --->  {'clusterSubnetsComplete': True, 'unresolveds': [{'serverIPMetadata': {'origin': 'external,external,external,external,external,external,external,external,external,external,external,external,external,external,external,external', 'ip': '52.216.142.166,52.216.143.166,52.216.144.245,52.216.147.13,52.216.177.117,52.216.225.115,52.216.242.14,52.216.248.190,52.216.26.174,52.217.16.198,52.217.163.0,52.217.166.144,52.217.171.80,52.217.202.144,52.217.80.238,54.231.134.8'}, 'clientProcess': 'stress,stress,stress,stress,stress,stress,stress,stress,stress,stress,stress,stress,stress,stress,stress,stress', 'serverPort': {'port': 80, 'protocol': 'TCP'}, 'alias': 'AWS', 'rowId': 'eu_external_AWS_80'}]}
                """
            egress_unused_data = getEgressUnusedInfo(k8s_cluster, k8s_namespace['name'], k8s_app_owner['name'], k8s_app_owner['kind'])
            if len(egress_unused_data['unresolveds']) > 0:
                print("egress unused ---> ", egress_unused_data)
            print("\n\n\n\n")

    print(temp_h)
