READ ME file 

## logging to the ginger site in order to download 
User:  
detroit@caninetofive.com
Password:   
313Canine 

Ferndale:   
https://ctfferndale.gingrapp.com/auth/login

Detroit:    
https://ctfdetroit.gingrapp.com/auth/login


FER.sql.gz
DET.sql.gz 

in 
dest="/home/$USER/scripts/update-gingr-db/"

## Installation of the playwright 

1. it is installed under python3.8 
2. Three additional libraries are installed

There was an error: after first run 
Host system is missing dependencies to run browsers. ║
║ Missing libraries:                                   ║
║     libdrm.so.2                                      ║
║     libgbm.so.1                                      ║
║     libasound.so.2 


https://installati.one/centos/7/libdrm/

wokred for first and second one 
sudo dnf makecache

sudo dnf -y install libdrm
sudo dnf -y install libgbm

for the third one 
sudo dnf -y install alsa-lib

