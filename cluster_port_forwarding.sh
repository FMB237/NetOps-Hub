#!/bin/bash 
#
#This is the cluster System Port Forwarding Scripts
#

kubectl port-forward -n netops-hub svc/netops-hub 8000:8000
