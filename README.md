![Home Assistant Dashboard](https://github.com/Doudou14/Domoticz-apsystems_ecu/blob/main/dashboard.jpg)
# Domoticz APsystems ECU Integration
This is an integration for [Domoticz](https://domoticz.com/) that adds support for the [APsystems](http://www.apsystems.com) Energy Communication Unit (ECU) so that you are able to monitor your PV installation (inverters) in detail. It currently supports ECU B - ECU C and ECU R
The installation procedure is based on [bjorn-meiger](https://www.bjorn-meijer.nl/en/2021/05/01/realtime-readout-apsystems-in-domoticz/)

## Add dummy sensors in Domoticz
* Create a Dummy sensor in Domoticz and call it 'Virtual switches' or another clear name.
Add dummy sensor in Domoticz
* Create a virtual sensor of the type 'Electric (Current + counter)'. Name the sensor 'Solar generation'.
* Create a virtual sensor of type 'Switch' and name it 'Inverter [number inverter]'. Repeat this step for the number of microinverters you have.
* Create a virtual sensor of the type 'Consumption (Electric)' and name it 'Inverter [number inverter] – Power [panel number]'. Repeat this step for the number of panels per microinverter.
* Create a virtual sensor of type 'Temperature' and name it 'Inverter [number inverter] – Temperature'. Repeat this step for the number of microinverters you have.
* Create a virtual sensor of type 'Text' and name it 'Timestamp'.
* Create a virtual sensor of type 'Percentage' and name it 'Inverter [number inverter] – Signal'. Repeat this step for the number of microinverters you have.
* Create a virtual sensor of type 'Voltage' and name it 'Inverter [number inverter] – Voltage'. Repeat this step for the number of microinverters you have.
* Create a virtual sensor of type 'Custom Sensor' and name it 'Inverter [number inverter] – Frequency' and add '%' on 'Axis Label' . Repeat this step for the number of microinverters you have.
* Note all idx http://IP-Domoticz:8080/#/Devices

## Install Plugin
To run the python scripts on the Raspberry Pi Python 3.x to be installed.
* Place APSystemECU.py and ECU-C-R.py or ECU-B (choose file from your ECU model) in your Domoticz folder under scripts/python/ECU
* If ECU C or R open ECU-C-R.py or If ECU B open ECU-B.py and change :
ecu_ip
url
idx with your custom sensor values

## Start script
If ECU C or R : Start the script with the command python3 /scripts/python/ECU/ECU-C-R.py
If ECU B : Start the script with the command python3 /scripts/python/ECU/ECU-B.py

## Auto start
To have the script start automatically after every reboot of the Raspberry Pi, add the following line in crontab
* Sudo crontab -e
* If ECU C or R Add : @reboot python3 /home/pi/domoticz/scripts/python/ECU/ECU-C-R.py
* If ECU B Add : @reboot python3 /home/pi/domoticz/scripts/python/ECU/ECU-B.py
* Reboot the pi
