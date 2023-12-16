packer {
  required_plugins {
    vagrant = {
      source  = "github.com/hashicorp/vagrant"
      version = "~> 1"
    }
  }
}

variable "salt_version" {
  type    = string
  default = "3006.5"
}

source "vagrant" "ubuntu2204" {
  communicator = "ssh"
  output_dir   = "build/${var.salt_version}"
  provider     = "virtualbox"
  source_path  = "ubuntu/jammy64"
}

build {
  sources = ["source.vagrant.ubuntu2204"]

  provisioner "shell" {
    inline = ["sudo apt-get update", "sudo apt-get install curl -y", "curl -o /tmp/bootstrap-salt.sh -L https://bootstrap.saltproject.io", "sudo sh /tmp/bootstrap-salt.sh -X -p git stable ${var.salt_version}"]
  }

  post-processor "vagrant-cloud" {
    architecture        = "amd64"
    box_tag             = "genaumann/ubuntu2204-salt"
    version             = "${var.salt_version}"
    version_description = "Ubuntu 22.04 testing image for Salt Formulas"
    keep_input_artifact = false
  }
}
