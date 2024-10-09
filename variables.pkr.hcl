variable "salt_version" {
  type        = string
  description = "Salt Version to install"
}

variable "src" {
  type        = string
  description = "Source vagrant box"
}

variable "os_short" {
  type        = string
  description = "Short OS code"
}

variable "pkg_mgr" {
  type    = string
  default = "apt"
}

variable "vagrant_cloud_client_id" {
  type        = string
  description = "Vagrant Cloud Client ID"
}

variable "vagrant_cloud_client_secret" {
  type        = string
  description = "Vagrant Cloud Client Secret"
}
