#!/bin/bash

python aci_app_packager.py -f /root/genaci/app/GeniNacTrigger
rm -rf *.pyc
rm -rf *.log
