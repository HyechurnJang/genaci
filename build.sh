#!/bin/bash

rm -rf Ciscokr-GeniNacTrigger-*.aci
git pull
python aci_app_packager.py -f GeniNacTrigger
