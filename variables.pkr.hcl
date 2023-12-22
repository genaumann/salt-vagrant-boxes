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
