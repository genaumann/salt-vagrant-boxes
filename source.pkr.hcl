source "vagrant" "image" {
  communicator = "ssh"
  output_dir   = "build/${var.os_short}/${var.salt_version}"
  provider     = "virtualbox"
  source_path  = "${var.src}"
}
