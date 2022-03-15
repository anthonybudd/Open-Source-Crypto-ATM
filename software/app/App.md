
# locla dev 
docker build -t pdf .
docker run pdf
docker run -v $(pwd):/output openlabs/docker-wkhtmltopdf -q --page-height 150 --page-width 100 /output/wallet.html /output/wallet.pdf



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

### Disable screensave

Open up /etc/lightdm/lightdm.conf using your favorite text editor (I prefer nano).
xserver-command=X -s 0 dpms

### Set background

## Roate Display



