# CEC Monitoring over HDMI for Raspberry Pi
This script can monitor a TV using the HDMI port of a Raspberry PI and toggle SmartThings devices when the TV turns on.

I have successfully used this script on Raspian Stretch lite.

## Installation
This script requires a few prerequisite python packages AND system pakages to run properly

### System Packages
cec-utils must be installed before the python-cec library will function.

### Python Packages
This script uses python3. Depending on how you have your python envioronment configured you will either need to uses pip3 install, or whatever package manager program is appropriate to your configuration, to pull the packages listed in thr requirements.rxt file.

```
pip3 install requirements.txt
```

see https://github.com/trainman419/python-cec for details about python-cec for rpi.

### Configuring the script
Copy the config_template.py file and create a new copy of the file called config.py in the same forlder as the HDMI CEC monitr script. Edit the file in a text editor such as nano and replace the parameters as follows:

Smarththings token can be generated using [this link](https://account.smartthings.com/tokens) be sure the token can read and execute commands for devices. 

The Device IDs can be found in the [SmartThings Developer portal](https://developers.smartthings.com/) Navigate to the list of devices and drill down to the device you would like to control (must be a light). You can obtain the device ID from the URL of the device (URL looks like ....api.smartthings.com/device/show/{device_id}

## Creating a systemd service

use the command: ```sudo nano /lib/systemd/system/tv_cec.service ```

to create a new service that will run on boot.
Enter the following:

```
 [Unit]
 Description=tv and light controll
 After=multi-user.target

 [Service]
 Type=idle
 ExecStart=/usr/bin/python3 /home/pi/pi-tv-smart-switch/hdmi_cec_monitor.py
 User=pi

 [Install]
 WantedBy=multi-user.target
```

## Troubleshooting
**Powering the PI:**

I found that I was unable to rely on the USB port of my TV to provide sufficent power to the USB port to power my PIi The Pi worked fine while the TV was on but would reboot intermittently when the TB was in standby. This was fixed by using an external AC wall charger for the Pi.

**HDMI CEC causing TV input switching or pi rebooting:**

It was neccessary to add the following line to the botton of the file **/boot/config.txt**
```
hdmi_ignore_cec_init=1
```