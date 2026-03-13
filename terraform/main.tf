provider "vsphere" {
  user           = var.vc_user
  password       = var.vc_password
  vsphere_server = var.vc_server
  allow_unverified_ssl = true
}

data "vsphere_datacenter" "dc" {
  name = var.vc_dc
}

data "vsphere_distributed_virtual_switch" "dvs" {
  name          = var.vc_dvs
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_resource_pool" "pool" {
  name          = var.vc_pool
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_datastore" "datastore" {
  name          = var.vc_datastore
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_network" "MNG" {
  name          = var.vc_mng
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_virtual_machine" "SB-Ubuntu-Template" {
  name          = "SB-Ubuntu-Template"
  datacenter_id = data.vsphere_datacenter.dc.id
}

#####################################################################################


# create node SB-ContainerLab
resource "vsphere_virtual_machine" "SB-ContainerLab" {
  name             = "SB-ContainerLab"
  resource_pool_id = data.vsphere_resource_pool.pool.id
  datastore_id     = data.vsphere_datastore.datastore.id
  num_cpus = 8
  memory   = 16384
  guest_id = data.vsphere_virtual_machine.SB-Ubuntu-Template.guest_id
  folder = "USER_VMs/SB"
  wait_for_guest_net_timeout = 0  
  network_interface {
    network_id   = data.vsphere_network.MNG.id
    adapter_type = "vmxnet3"
  } 
  disk {
    label = "Hard disk 1"
    size             = 128
    thin_provisioned = true
  }

  annotation = "Deploy via Terraform, Project: ContainerLab-2026"

  clone {
    template_uuid = data.vsphere_virtual_machine.SB-Ubuntu-Template.id
    customize {
      linux_options {
        host_name = "SB-ContainerLab"
        domain    = "lab"
      }
      network_interface {
        ipv4_address = "10.208.116.71"
        ipv4_netmask = 24
      }

      ipv4_gateway = "10.208.116.1"
      dns_server_list = ["10.208.116.10", "8.8.8.8"]
    }
  }
}
