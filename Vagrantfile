# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network :private_network, ip: "192.168.33.30"
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--name", "comedylib", "--memory", "1024"]
  end

  config.vm.synced_folder "../comedylib", "/var/www/comedylib"
  config.ssh.private_key_path = ["~/.vagrant.d/insecure_private_key", "~/.ssh/id_rsa"]
  config.ssh.insert_key = false
  config.ssh.forward_agent = true

  # Ansible provisioner.
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "ansible/development.yml"
    ansible.inventory_path = "ansible/inventory/development"
    ansible.limit = "development"
    ansible.host_key_checking = false
    ansible.verbose = "v"
    ansible.raw_arguments = ["--timeout=100"]
  end
end
