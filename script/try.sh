#!/bin/bash  
HOME=/home/pi
LOGNAME=pi
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
LANG=en_US.UTF-8
SHELL=/bin/sh
PWD=/pi
cd /home/pi/CODA/cod-autorganizzato.github.io/script
git pull
python create_json.py
git add /home/pi/CODA/cod-autorganizzato.github.io/JSON/data.json
git commit -m "aggiornati dati" -m "check check one two one two";
git push https://cod-autorganizzato:AntifascismoPappapero@github.com/cod-autorganizzato/cod-autorganizzato.github.io












