# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

# ---- Define number of nodes to spin up ----
N = 3

# ---- Define any custom memory/cpu requirement ----
# if custom requirements are desired...ensure to set
# custom_cpu_mem == "yes" otherwise set to "no"
# By default if custom requirements are defined and set below
# any node not defined will be configured as the default...
# which is 1vCPU/512mb...So if setting custom requirements
# only define any node which requires more than the defaults.
nodes = [
  {
    :node => "node0",
    :cpu => 1,
    :mem => 1024
  }
]

# ---- Define variables below ----
additional_disks = "no"  #Define if additional drives defined should be added (yes | no)
additional_disks_controller = "SATA Controller"
additional_disks_num = 1  #Define the number of additional disks to add
additional_disks_size = 10  #Define disk size in GB
additional_nics = "yes"  #Define if additional network adapters should be created (yes | no)
additional_nics_num = 1  #Define the number of additional nics to add
box = "mrlesmithjr/trusty64"  #Define Vagrant box to load
custom_cpu_mem = "yes"  #Define if custom cpu and memory requirements are needed (yes| no)...defined within nodes variable above
desktop = "no"  #Define if running desktop OS (yes | no)
enable_port_forwards = "yes"  #Define if port forwards should be enabled
linked_clones = "no"  #Defines if nodes should be linked from master VM (yes | no)
port_forwards = [
  {
    :node => "node0",
    :guest => 80,
    :host => 8080
  }
]
provision_nodes = "yes"  #Define if provisioners should run (yes | no)
server_cpus = 1  #Define number of CPU cores...will be ignored if custom_cpu_mem == "yes"
server_memory = 512  #Define amount of memory to assign to node(s)...will be ignored if custom_cpu_mem == "yes"
subnet = "192.168.202."  #Define subnet for private_network
subnet_ip_start = 200  #Define starting last octet of the subnet range to begin addresses for node(s)

Vagrant.configure(2) do |config|

  #Iterate over nodes
  (1..N).each do |node_id|
    nid = (node_id - 1)

    config.vm.define "node#{nid}" do |node|
      node.vm.box = box
      node.vm.provider "virtualbox" do |vb|
        if linked_clones == "yes"
          vb.linked_clone = true
        end
        if custom_cpu_mem == "no"
          vb.customize ["modifyvm", :id, "--cpus", server_cpus]
          vb.customize ["modifyvm", :id, "--memory", server_memory]
        end
        if custom_cpu_mem == "yes"
          nodes.each do |cust_node|
            if cust_node[:node] == "node#{nid}"
              vb.customize ["modifyvm", :id, "--cpus", cust_node[:cpu]]
              vb.customize ["modifyvm", :id, "--memory", cust_node[:mem]]
            end
          end
        end
        if desktop == "yes"
          vb.gui = true
          vb.customize ["modifyvm", :id, "--graphicscontroller", "vboxvga"]
          vb.customize ["modifyvm", :id, "--accelerate3d", "on"]
          vb.customize ["modifyvm", :id, "--ioapic", "on"]
          vb.customize ["modifyvm", :id, "--vram", "128"]
          vb.customize ["modifyvm", :id, "--hwvirtex", "on"]
        end
        if additional_disks == "yes"
          (1..additional_disks_num).each do |disk_num|
            dnum = (disk_num + 1)
            ddev = ("node#{nid}_Disk#{dnum}.vdi")
            unless File.exist?("#{ddev}")
              vb.customize ['createhd', '--filename', ("#{ddev}"), '--variant', 'Fixed', '--size', additional_disks_size * 1024]
            end
            vb.customize ['storageattach', :id,  '--storagectl', "#{additional_disks_controller}", '--port', dnum, '--device', 0, '--type', 'hdd', '--medium', "node#{nid}_Disk#{dnum}.vdi"]
          end
        end
      end
      node.vm.hostname = "node#{nid}"

      ### Define additional network adapters below
      if additional_nics == "yes"
        (1..additional_nics_num).each do |nic_num|
          nnum = Random.rand(0..50)
          node.vm.network :private_network, ip: subnet+"#{subnet_ip_start + nid + nnum}"
        end
      end

      ### Define port forwards below
      if enable_port_forwards == "yes"
        port_forwards.each do |pf|
          if pf[:node] == "node#{nid}"
            node.vm.network "forwarded_port", guest: pf[:guest], host: pf[:host] + nid
          end
        end
      end
      if provision_nodes == "yes"
        if node_id == N
          node.vm.provision "ansible" do |ansible|  #runs bootstrap Ansible playbook
            ansible.limit = "all"
            ansible.playbook = "bootstrap.yml"
          end
          node.vm.provision "ansible" do |ansible|  #runs Ansible playbook for installing roles/executing tasks
            ansible.limit = "all"
            ansible.playbook = "playbook.yml"
            ansible.groups = {
              "ddi-nodes" => [
                "node0"
              ]
            }
          end
        end
      end

    end
  end
  if provision_nodes == "yes"
    config.vm.provision :shell, path: "bootstrap.sh", keep_color: "true"  #runs initial shell script
  end
end
