Purpose
=======

Spins up single/multi node instance(s) of an Open-Source DDI (DNS, DHCP and IPAM)  
solution. This includes PowerDNS (DNS), ISC-DHCP (DHCP) and phpIPAM (IPAM).    
https://www.powerdns.com/  
http://phpipam.net/  
https://www.isc.org/downloads/dhcp/  

Once everything is installed you can pull up the following interfaces  
using your browser of choice.  

###### PowerDNS NSEdit
http://127.0.0.1:8080/nsedit  (admin/admin)

###### phpIPAM

http://127.0.0.1:8080/phpipam/?page=login  (admin/ipamadmin)

Interested in learning the API for PowerDNS?
https://doc.powerdns.com/md/httpapi/README/

Quick How-To
============
````
git clone https://github.com/mrlesmithjr/vagrant-ansible-ddi.git
cd vagrant-ansible-ddi
````
You can spin up a single DDI node with 2 nodes for testing DDI functionality  
by...  
````
./ddi_single.sh
````
You can spin up a DDI cluster with 3 DDI nodes and 2 nodes for testing DDI  
functionality by...
````
./ddi_cluster.sh
````
When you are done using the Vagrant environment...Tear it down quickly...
````
./cleanup.sh
````
You can also define the following Vagrant boxes for testing by changing the  
following line in the respective Vagrantfile...
````
box = "mrlesmithjr/trusty64"
````
The following will work with this lab...
````
mrlesmithjr/centos-7 (CentOS 7)
mrlesmithjr/jessie64 (Debian Jessie)
mrlesmithjr/trusty64 (Ubuntu Trusty)
````
If using CentOS you will need to modify the following line in the respective  
playbook.yml...
````
galera_cluster_bind_address: '{{ ansible_eth1.ipv4.address }}'  #'{{ ansible_enp0s8.ipv4.address }}'
````
Debian/Ubuntu
````
galera_cluster_bind_address: '{{ ansible_eth1.ipv4.address }}'
````
CentOS
````
galera_cluster_bind_address: '{{ ansible_enp0s8.ipv4.address }}'
````

Requirements
============

The following packages must be installed on your Host you intend on running all  
of this from. If Ansible is not available for your OS (Windows) you can check  
out the following..  
http://everythingshouldbevirtual.com/ansible-using-ansible-on-windows-via-cygwin

Ansible (http://www.ansible.com/home)

VirtualBox (https://www.virtualbox.org/)

Vagrant (https://www.vagrantup.com/)

````
playbook.yml
````
Adjust the variables under vars: to suit your needs. By Default PowerDNS and  
phpIPAM are installed.  
````
---
- hosts: all
  become: true
  vars:
    - pri_domain_name: 'test.vagrant.local'
  roles:
  tasks:
    - name: pre-reqs
      dnf:
        name: "{{ item }}"
        state: present
      with_items:
        - libselinux-python
      when: >
            (ansible_os_family == "RedHat" and
            ansible_distribution == "Fedora")

    - name: pre-reqs
      yum:
        name: "{{ item }}"
        state: present
      with_items:
        - libselinux-python
      when: >
            (ansible_os_family == "RedHat" and
            ansible_distribution != "Fedora")

    - name: updating /etc/hosts
      lineinfile:
        dest: /etc/hosts
        regexp: "^{{ hostvars[item].ansible_ssh_host }} {{ item }} {{ item }}.{{ pri_domain_name }}"
        line: "{{ hostvars[item].ansible_ssh_host }} {{ item }} {{ item }}.{{ pri_domain_name }}"
        state: present
      with_items: groups['all']

- hosts: ddi-nodes
  become: true
  handlers:
    - name: 'restart pdns'
      service:
        name: "pdns"
        state: "restarted"
        sleep: 10
  remote_user: vagrant
  vars:
    - deb_db_password: $6$3BFlAptb$S4313dXRWU12lLTXbh2/h3mBOdUWA1pQMQ7uYwWVT32Ko.R.cRdIZETFHKbgdpWRNbRe6XoKECIEFxqgFu2vp.
    - enable_pdns_server_logging: true
    - enable_pdns_web_server: true
    - install_dhcp: false  #defines if dhcp services should be installed
    - install_dns: true  #defines if powerdns (dns) services should be installed
    - install_logstash: false  #defines if logstash should be installed to monitor powerdns
    - install_phpipam: true  #defines if phpipam services should be installed
    - install_quagga: false  #defines if quagga (routing) should be installed for AnyCast services
    - mysql_root_password: $6$3BFlAptb$S4313dXRWU12lLTXbh2/h3mBOdUWA1pQMQ7uYwWVT32Ko.R.cRdIZETFHKbgdpWRNbRe6XoKECIEFxqgFu2vp.
    - pdns_db_name: pdns
    - pdns_db_pass: pdns
    - pdns_db_user: pdns
    - phpipam_define_cron_jobs: true
    - phpipam_pre_load_db: true
    - phpipam_url_rewrite: true
    - phpipam_version: 1.2.1
    - pri_domain_name: vagrant.local
  roles:
    - role: ansible-etc-hosts
    - role: ansible-apache2
    - role: ansible-config-interfaces
    - role: ansible-mariadb-mysql
    - role: ansible-isc-dhcp
      when: >
            install_dhcp is defined and
            install_dhcp
    - role: ansible-logstash
      when: >
            install_logstash is defined and
            install_logstash
    - role: ansible-phpipam
      when: >
            install_phpipam is defined and
            install_phpipam
    - role: ansible-powerdns
      when: >
            install_dns is defined and
            install_dns
    - role: ansible-quagga
      when: >
            (install_quagga is defined and
            install_quagga) and
            (enable_pdns_anycast is defined and
            enable_pdns_anycast)
  tasks:
    - name: Allowing PDNS to listen on all interfaces
      lineinfile:
        dest: "/etc/powerdns/pdns.conf"
        regexp: "^local-address="
        line: "local-address=0.0.0.0"
      notify: restart pdns
````

Usage
=====

http://everythingshouldbevirtual.com/learning-vagrant-and-ansible-provisioning

````
git clone https://github.com/mrlesmithjr/vagrant-ansible-ddi.git
cd vagrant-ansible-ddi
````
Spin up your environment
````
vagrant up
````
When you are done using the Vagrant environment...Tear it down quickly...
````
./cleanup.sh
````

The default Vagrant box is..  
````
box = "mrlesmithjr/trusty64"
````
You can change this to any of the following to test Debian/Ubuntu/CentOS by  
editing the Vagrantfile..  
````
box = "mrlesmithjr/centos-7" (CentOS 7)
box = "mrlesmithjr/jessie64" (Debian Jessie)
box = "mrlesmithjr/trusty64" (Ubuntu Trusty)
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
