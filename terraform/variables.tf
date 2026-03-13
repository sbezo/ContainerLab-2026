variable "vc_user" {
  description = "vCenter user login"
  type        = string
}

variable "vc_password" {
  description = "vCenter user password"
  type        = string
  sensitive   = true
}

variable "vc_server" {
  description = "vCenter server"
  type        = string
}

variable "vc_dc" {
  description = "vCenter DC"
  type        = string
}

variable "vc_dvs" {
  description = "vCenter Distributed Virtual Switch"
  type        = string
}

variable "vc_pool" {
  description = "vCenter Pool"
  type        = string
}

variable "vc_datastore" {
  description = "vCenter DataStore"
  type        = string
}

variable "vc_mng" {
  description = "vCenter Management DPG"
  type        = string
}
