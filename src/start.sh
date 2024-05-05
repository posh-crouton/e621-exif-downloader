#!/bin/bash

sudo apt install libimage-exiftool-perl=12.40+dfsg-1 python3.10-venv # required to create venv

python3 -m venv myenv
source myenv/bin/activate
python3 -m pip install -r requirements.txt

python3 main.py

deactivate