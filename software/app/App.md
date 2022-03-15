# App

*Below are just notes I will clean this up and make a bash script later*


sudo apt-get install wkhtmltopdf
pip3 install bitcoinlib
pip3 install qrcode
pip3 install python-dotenv

set disable_overscan=1 in /boot/config.txt

### Auto Run
sudo nano /lib/systemd/system/atm.service

[Unit]
 Description=My Sample Service
 After=multi-user.target

 [Service]
 Type=idle
 ExecStart=/usr/bin/python3 /home/pi/app/app.py

 [Install]
 WantedBy=multi-user.target


### Disable Cursor
/etc/lightdm/lightdm.conf
xserver-command = X -nocursor

### Disable screensaver

Open up /etc/lightdm/lightdm.conf using your favorite text editor (I prefer nano).
xserver-command=X -s 0 dpms

### Set background

### Roate Display



