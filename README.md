# CEC Monitoring over HDMI for Raspberry Pi
This script can monitor a TV using an HDMI connection  and toggle SmartThings devices when the TV turns on.

I have tested this script with the Raspian Stretch lite distro.

## Installation
This script requires a few prerequisite python packages AND system packages to run properly.

### System Packages
cec-utils must be installed before the python-cec library will function.

### Python Packages
This script uses python3. Depending on how you have your python environment configured you will either need to uses pip3 install, or whatever command is appropriate to your environment configuration, to pull the packages listed in the requirements.rxt file.

```
pip3 install -r requirements.txt
```

see https://github.com/trainman419/python-cec for more details about python-cec for rpi.

### Configuring the script
Copy the config_template.py file and create a new copy of the file called config.py in the same folder as the HDMI CEC monitor script. Edit the file in a text editor such as nano and replace the parameters as follows:

SmartThings tokens can be generated using [this link](https://account.smartthings.com/tokens) be sure the token can read and execute commands for devices. 

The Device IDs can be found in the [SmartThings Developer portal](https://developers.smartthings.com/) Navigate to the list of devices and drill down to the device you would like to control (must be a light). You can obtain the device ID from the URL of the device (URL looks like ....api.smartthings.com/device/show/{device_id}

## Creating a systemd service

use the command: ```sudo nano /lib/systemd/system/tv_cec.service ```

to create a new service that will run on boot.
Enter the following:

```
 [Unit]
 Description=tv and light control
 After=multi-user.target

 [Service]
 Type=idle
 ExecStart=/usr/bin/python3 /home/pi/pi-tv-smart-switch/hdmi_cec_monitor.py
 User=pi

 [Install]
 WantedBy=multi-user.target
```
Then run:

```
sudo systemctl daemon-reload
```
```
sudo systemctl start tv_cec.service
```


## Troubleshooting
**Powering the PI:**

I found that I was unable to rely on the 800ma rated USB port of my Sony 2017 model TV to provide sufficient power to the USB port to power my Pi zero W. The Pi worked fine while the TV was on but would reboot intermittently when the TV was in standby. This was fixed by using an external AC wall charger for the Pi.

**HDMI CEC causing TV input switching or pi rebooting:**

It was necessary to add the following line to the bottom of the file **/boot/config.txt**
```
hdmi_ignore_cec_init=1
```