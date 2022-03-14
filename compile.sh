#!/bin/bash

########################################
############# CSCI 2951-O ##############
########################################

# install Python3.8
wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz
tar xzf Python-3.8.12.tgz
pushd Python-3.8.12
./configure --enable-optimizations
make altinstall
popd

pip3.8 install -r requirements

(cd cplex; python3.8 setup.py install)