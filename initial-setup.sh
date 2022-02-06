#!/bin/bash
sudo apt-get install gettext 
python3 -m venv .env   
source .env/bin/activate 
pip3 install -r requirements.txt  
python3 manage.py makemigrations && python3 manage.py migrate  
python3 manage.py loaddata default.json
python3 manage.py createsuperuser  