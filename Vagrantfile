# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  config.vm.define "ddi" do |ddi|
    ddi.vm.box = "mrlesmithjr/trusty64"
    ddi.vm.hostname = "ddi"

    ddi.vm.network :private_network, ip: "192.168.202.201"
    ddi.vm.network "forwarded_port", guest: 80, host: 8080

    ddi.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
    end
  end
  config.vm.provision :shell, path: "provision.sh"
end
