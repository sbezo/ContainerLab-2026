include .env
export

tf-init:
	terraform -chdir=./terraform init

tf-apply:
	terraform -chdir=./terraform apply

setup-ansible:
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	pip3 install ansible && \
	pip3 install ansible-vault

upgrade-packages:
	source .venv/bin/activate && \
	cd ansible && \
	ansible-playbook -i inventories/hosts.yml --vault-password-file .ansible_vault playbooks/upgrade_packages.yml

install-docker:
	source .venv/bin/activate && \
	cd ansible && \
	ansible-playbook -i inventories/hosts.yml --vault-password-file .ansible_vault playbooks/install_docker.yml

install-containerlab:
	source .venv/bin/activate && \
	cd ansible &&  \
	ansible-playbook -i inventories/hosts.yml --vault-password-file .ansible_vault playbooks/install_containerlab.yml
	
prepare-iosxrd:
	source .venv/bin/activate && \
	cd ansible &&  \
	ansible-playbook -i inventories/hosts.yml --vault-password-file .ansible_vault playbooks/prepare_iosxrd.yml

copy-labs:
	source .venv/bin/activate && \
	cd ansible &&  \
	ansible-playbook -i inventories/hosts.yml --vault-password-file .ansible_vault playbooks/copy_labs.yml










