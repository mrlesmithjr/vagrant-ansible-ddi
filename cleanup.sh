#!/bin/bash
vagrant destroy -f
for file in *.retry; do
  if [[ -f $file ]]; then
    rm $file
  fi
done
if [ -d host_vars ]; then
  rm -rf host_vars
fi
if [ -d .vagrant ]; then
  rm -rf .vagrant
fi
if [ -f playbook.yml ]; then
  rm playbook.yml
fi
if [ -f Vagrantfile ]; then
  rm Vagrantfile
fi
