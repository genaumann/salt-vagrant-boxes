locals {
  pre_install  = var.pkg_mgr == "apt" ? "sudo apt-get update" : ""
  curl_install = var.pkg_mgr == "apt" ? "sudo apt-get install curl -y" : var.pkg_mgr == "dnf" ? "sudo dnf install curl -y" : var.pkg_mgr == "zypper" ? "sudo zypper -n install curl git-core" : ""
}

build {
  sources = ["source.vagrant.image"]

  provisioner "shell" {
    inline = [
      local.pre_install,
      local.curl_install,
      "curl -o /tmp/bootstrap-salt.sh -L https://bootstrap.saltproject.io",
      "sudo sh /tmp/bootstrap-salt.sh -X -p git stable ${var.salt_version}",
      "sudo salt-call --local pip.install requests==2.31.0" // docker error on requests > 2.31.0 - see https://github.com/geerlingguy/ansible-role-docker/issues/462
    ]
  }

  post-processor "vagrant-registry" {
    architecture        = "amd64"
    box_tag             = "genaumann/${var.os_short}-salt"
    version             = "${var.salt_version}"
    version_description = "${var.os_short} testing image for Salt Formulas"
    keep_input_artifact = false
    client_id           = var.vagrant_cloud_client_id
    client_secret       = var.vagrant_cloud_client_secret
  }
}
