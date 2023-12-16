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

source "vagrant" "debian12" {
  communicator = "ssh"
  output_dir   = "build/${var.salt_version}"
  provider     = "virtualbox"
  source_path  = "debian/bookworm64"
}

build {
  sources = ["source.vagrant.debian12"]

  provisioner "shell" {
    inline = ["sudo apt-get update", "sudo apt-get install curl -y", "curl -o /tmp/bootstrap-salt.sh -L https://bootstrap.saltproject.io", "sudo sh /tmp/bootstrap-salt.sh -X -p git stable ${var.salt_version}"]
  }

  post-processor "vagrant-cloud" {
    architecture        = "amd64"
    box_tag             = "genaumann/debian12-salt"
    version             = "${var.salt_version}"
    version_description = "Debian 12 testing image for Salt Formulas"
    keep_input_artifact = false
  }
}
