Purpose
=======

Spins up a single node instance of an Open-Source DDI (DNS, DHCP and IPAM) solution. This includes PowerDNS (DNS), ISC-DHCP (DHCP) and phpIPAM (IPAM).
https://www.powerdns.com/
http://phpipam.net/
https://www.isc.org/downloads/dhcp/

Once everything is installed you can pull up the following interfaces using your browser of choice.

###### PowerDNS NSEdit
http://192.168.202.201/nsedit  (admin/admin)

###### phpIPAM

http://192.168.202.201/phpipam  (admin/ipamadmin)

Interested in learning the API for PowerDNS?
https://doc.powerdns.com/md/httpapi/README/

Quick How-To
============
````
git clone https://github.com/mrlesmithjr/vagrant-ansible-ddi.git
cd vagrant-ansible-ddi
vagrant up
````
Requirements
============

The following packages must be installed on your Host you intend on running all of this from. If Ansible is not available for your OS (Windows) you can check out the following http://everythingshouldbevirtual.com/ansible-using-ansible-on-windows-via-cygwin .

Ansible (http://www.ansible.com/home)

VirtualBox (https://www.virtualbox.org/)

Vagrant (https://www.vagrantup.com/)

````
playbook.yml
````
Adjust the variables under vars: to suit your needs. By Default PowerDNS and phpIPAM are installed.
````
---
- hosts: all
  become: true
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
    - role: ansible-etc-hosts
    - role: ansible-apache2
    - role: ansible-config-interfaces
    - role: ansible-mariadb-mysql
    - role: ansible-isc-dhcp
      when: install_dhcp is defined and install_dhcp
    - role: ansible-logstash
      when: install_logstash is defined and install_logstash
    - role: ansible-phpipam
      when: install_phpipam is defined and install_phpipam
    - role: ansible-powerdns
      when: install_dns is defined and install_dns
    - role: ansible-quagga
      when: >
            (install_quagga is defined and install_quagga) and
            (enable_pdns_anycast is defined and enable_pdns_anycast)
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

License
-------

BSD

Author Information
------------------

Larry Smith Jr.
- @mrlesmithjr
- http://everythingshouldbevirtual.com
- mrlesmithjr [at] gmail.com
