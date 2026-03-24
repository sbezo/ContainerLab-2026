# About
This repo provides end-to-end procedure for building Containerlab topology with ios-xrd docker image.
Lab is deployed on remote Linux server on ESXi hypervisor in my case.
Everything what makes sense is deployed remotly (Terraform/Ansible)

# Deployment notes:
ios-xrd image is too big for github, so download your own
_.env_example should be configure before deployment and change to .env

# Preparation procedure from local host
Follow makefile to:
- Linux host provisioning via Terraform
- Ansible deployment of:
    - docker
    - containerlab
- Ansible copy and prepare of ios-xrd image to remote host
- Ansible Copy dir with lab topologies


#############################################
# Operating containerlab from local host
#############################################

## copy lab folder from local host
make copy-labs

## deploy lab from local host
make deploy-lab TOPO=test-lab.clab.yml

## open terminals from local host
make connect TOPO=test-lab.clab.yml




#############################################
# Operating containerlab on remote Linux host
#############################################

## destroy all labs and clean up
containerlab destroy -a -c

## run lab
containerlab deploy -t Topologies/test-lab.clab.yml

## lab containers should run now:
docker ps

## in case of topology change:
containerlab deploy -t Topologies/test-lab.clab.yml --reconfigure


## on remote Linux host:
containerlab deploy -t Topologies/test-lab.clab.yml --reconfigure

## destroy lab
containerlab destroy -t test-lab.clab.yml

## connect to router directly from Linux host:
ssh clab@clab-xrd-lab-r1
password: clab@123

## or remote to ports 2201 and 2202 (as defined in lab yml)
ssh clab@<Linux_host_IP> -p 2201



# Result

<img width="792" height="297" alt="image" src="https://github.com/user-attachments/assets/c98163e1-bd0b-43b4-bea6-0a3ab6dd07e4" />
