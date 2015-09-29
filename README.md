Purpose
=======

Spins up a single node instance of an Open-Source DDI (DNS, DHCP and IPAM) solution. This includes PowerDNS (DNS), ISC-DHCP (DHCP) and phpIPAM (IPAM).
https://www.powerdns.com/
http://phpipam.net/
https://www.isc.org/downloads/dhcp/

Once everything is installed you can pull up the following interfaces using your browser of choice.

###### PowerDNS NSEdit
http://192.168.202.33/nsedit  (admin/admin)

###### phpIPAM

http://192.168.202.33/phpipam  (admin/ipamadmin)

Interested in learning the API for PowerDNS?
https://doc.powerdns.com/md/httpapi/README/
Requirements
============

The following packages must be installed on your Host you intend on running all of this from. If Ansible is not available for your OS (Windows) You can modify the following lines in the Vagrantfile.

From:
````
#  config.vm.provision :shell, path: "bootstrap.sh"
#      node.vm.provision :shell, path: "bootstrap_ansible.sh"

config.vm.provision :ansible do |ansible|
  ansible.playbook = "bootstrap.yml"
end
````
To:
````
  config.vm.provision :shell, path: "bootstrap.sh"
      node.vm.provision :shell, path: "bootstrap_ansible.sh"

#config.vm.provision :ansible do |ansible|
#  ansible.playbook = "bootstrap.yml"
#end
````

Ansible (http://www.ansible.com/home)

VirtualBox (https://www.virtualbox.org/)

Vagrant (https://www.vagrantup.com/)



Variable Definitions
====================
````
nodes.yml
````
Define the nodes to spin up
````
---
# Keep in mind....Vagrant will always create an initial interface as a NAT interface..Any definitions below are for adding additional interfaces.
# for network_name define a var other than remaining blank to define an internal only network. Otherwise leave blank for a host-only network.
# for DHCP leave ip and network_name vars blank
# for Static define ip var
# type should generally be private_network..Other option(s) are: public_network
- name: node-1
  box: mrlesmithjr/trusty64
  mem: 1024
  cpus: 1
  ansible_ssh_host_ip: 192.168.202.33 #always create for Ansible provisioning within nodes
  config_interfaces: "False"  #defines if interfaces below should be created or not...Set to "False" if you do not wish to create the interfaces.
  interfaces:  #Define additional interface settings
    - ip: 192.168.12.11
      auto_config: "True"
      network_name: 01-to-02
      method: static
      type: private_network
    - ip: 192.168.14.11
      auto_config: "True"
      network_name:
      method: static
      type: private_network
    - ip: 192.168.15.11
      auto_config: "False"
      network_name: 01-to-05
      method: static
      type: private_network
    - ip:
      auto_config: "True"
      network_name:
      method: dhcp
      type: private_network
````

Provisions nodes by bootstrapping using Ansible
````
bootstrap.yml
````
Bootstrap Playbook
````
---
- hosts: all
  remote_user: vagrant
  sudo: yes
  vars:
    - galaxy_roles:
      - mrlesmithjr.apache2
      - mrlesmithjr.base
      - mrlesmithjr.bootstrap
      - mrlesmithjr.config-interfaces
      - mrlesmithjr.isc-dhcp
      - mrlesmithjr.logstash
      - mrlesmithjr.mariadb-mysql
      - mrlesmithjr.phpipam
      - mrlesmithjr.powerdns
      - mrlesmithjr.quagga
    - install_galaxy_roles: true
    - ssh_key_path: '.vagrant/machines/{{ inventory_hostname }}/virtualbox/private_key'
    - update_host_vars: true
  roles:
  tasks:
    - name: updating apt cache
      apt: update_cache=yes cache_valid_time=3600
      when: ansible_os_family == "Debian"

    - name: installing ansible pre-reqs
      apt: name={{ item }} state=present
      with_items:
        - python-pip
        - python-dev
      when: ansible_os_family == "Debian"

    - name: adding ansible ppa
      apt_repository: repo='ppa:ansible/ansible'
      when: ansible_os_family == "Debian"

    - name: installing ansible
      apt: name=ansible state=latest
      when: ansible_os_family == "Debian"

    - name: installing epel repo
      yum: name=epel-release state=present
      when: ansible_os_family == "RedHat"

    - name: installing ansible
      yum: name=ansible state=present
      when: ansible_os_family == "RedHat"

#    - name: installing ansible
#      pip: name=ansible state=present

#    - name: linking ansible hosts inventory
#      file: src=/etc/ansible/hosts path=/vagrant/ansible/hosts state=link

    - name: installing ansible-galaxy roles
      shell: ansible-galaxy install {{ item }} --force
      with_items: galaxy_roles
      when: install_galaxy_roles is defined and install_galaxy_roles

    - name: ensuring host file exists in host_vars
      stat: path=./host_vars/{{ inventory_hostname }}
      delegate_to: localhost
      register: host_var
      sudo: false
      when: update_host_vars is defined and update_host_vars

    - name: creating missing host_vars
      file: path=./host_vars/{{ inventory_hostname }} state=touch
      delegate_to: localhost
      sudo: false
      when: not host_var.stat.exists

    - name: updating ansible_ssh_port
      lineinfile: dest=./host_vars/{{ inventory_hostname }} regexp="^ansible_ssh_port{{ ':' }}" line="ansible_ssh_port{{ ':' }} 22"
      delegate_to: localhost
      sudo: false
      when: update_host_vars is defined and update_host_vars

    - name: updating ansible_ssh_host
      lineinfile: dest=./host_vars/{{ inventory_hostname }} regexp="^ansible_ssh_host{{ ':' }}" line="ansible_ssh_host{{ ':' }} {{ ansible_eth1.ipv4.address }}"
      delegate_to: localhost
      sudo: false
      when: update_host_vars is defined and update_host_vars and ansible_eth1 is defined

    - name: updating ansible_ssh_host
      lineinfile: dest=./host_vars/{{ inventory_hostname }} regexp="^ansible_ssh_host{{ ':' }}" line="ansible_ssh_host{{ ':' }} {{ ansible_enp0s8.ipv4.address }}"
      delegate_to: localhost
      sudo: false
      when: update_host_vars is defined and update_host_vars and ansible_enp0s8 is defined

    - name: updating ansible_ssh_key
      lineinfile: dest=./host_vars/{{ inventory_hostname }} regexp="^ansible_ssh_private_key_file{{ ':' }}" line="ansible_ssh_private_key_file{{ ':' }} {{ ssh_key_path }}"
      delegate_to: localhost
      sudo: false
      when: update_host_vars is defined and update_host_vars

    - name: ensuring host_vars is yaml formatted
      lineinfile: dest=./host_vars/{{ inventory_hostname }} regexp="---" line="---" insertbefore=BOF
      delegate_to: localhost
      sudo: false
      when: update_host_vars is defined and update_host_vars
````
````
playbook.yml
````
Adjust the variables under vars: to suit your needs. By Default PowerDNS and phpIPAM are installed.
````
---
- hosts: all
  sudo: true
  remote_user: vagrant
  vars:
    - deb_db_password: $6$3BFlAptb$S4313dXRWU12lLTXbh2/h3mBOdUWA1pQMQ7uYwWVT32Ko.R.cRdIZETFHKbgdpWRNbRe6XoKECIEFxqgFu2vp.
    - enable_pdns_web_server: true
    - install_dhcp: false  #defines if dhcp services should be installed
    - install_dns: true  #defines if powerdns (dns) services should be installed
    - install_logstash: false  #defines if logstash should be installed to monitor powerdns
    - install_phpipam: true  #defines if phpipam services should be installed
    - install_quagga: false  #defines if quagga (routing) should be installed for AnyCast services
    - mysql_root_password: $6$3BFlAptb$S4313dXRWU12lLTXbh2/h3mBOdUWA1pQMQ7uYwWVT32Ko.R.cRdIZETFHKbgdpWRNbRe6XoKECIEFxqgFu2vp.
  roles:
    - mrlesmithjr.apache2
    - mrlesmithjr.config-interfaces
    - mrlesmithjr.mariadb-mysql
    - { role: mrlesmithjr.isc-dhcp, when: install_dhcp is defined and install_dhcp }
    - { role: mrlesmithjr.logstash, when: install_logstash is defined and install_logstash }
    - { role: mrlesmithjr.phpipam, when: install_phpipam is defined and install_phpipam }
    - { role: mrlesmithjr.powerdns, when: install_dns is defined and install_dns }
    - { role: mrlesmithjr.quagga, when: (install_quagga is defined and install_quagga) and (enable_pdns_anycast is defined and enable_pdns_anycast) }
````

Usage
=====

http://everythingshouldbevirtual.com/learning-vagrant-and-ansible-provisioning

````
git clone https://github.com/mrlesmithjr/vagrant-ansible-ddi.git
cd vagrant-ansible-ddi
````
Update nodes.yml to reflect your desired nodes to spin up.

Spin up your environment
````
vagrant up
````

To run ansible from within Vagrant nodes (Ex. site.yml)
````
vagrant ssh
cd /vagrant
ansible-playbook -i hosts playbook.yml
````

To install ansible-galaxy roles within your HostOS
````
ansible-galaxy install mrlesmithjr.bootstrap
ansible-galaxy install mrlesmithjr.base
````

License
-------

BSD

Author Information
------------------

Larry Smith Jr.
- @mrlesmithjr
- http://everythingshouldbevirtual.com
- mrlesmithjr [at] gmail.com
