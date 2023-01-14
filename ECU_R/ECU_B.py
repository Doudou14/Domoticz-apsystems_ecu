#!/usr/bin/env python3
 
from APSystemsECU import APSystemsECU
import time
import asyncio
import urllib.request
import urllib.parse
import urllib
from pprint import pprint
 
 
ecu_ip = "IP ECU-B"
#Communication delay to ECU (sec)
sleep = 300
 
url = 'http://IP-Domoticz:8080/json.htm?'
puntcomma = '\u003B'
 
loop = asyncio.get_event_loop()
ecu = APSystemsECU(ecu_ip)
 
while True:
        try:
                data = loop.run_until_complete(ecu.async_query_ecu())
                #pprint(data)
 
                lifetime_energy = str(data.get('lifetime_energy')*1000)
                today_energy = str(data.get('today_energy')*1000)
                print('Today energy : ' + today_energy + ' Wh')
                current_power = str(data.get('current_power'))
                print('Current power: ' + current_power + ' W')
                generated_energy = (current_power + puntcomma + lifetime_energy)
                print('Total energy : ' + lifetime_energy + ' Wh')
                if (float(today_energy) >= 0 or float(current_power) >= 0):
                    getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 218, 'svalue': (generated_energy)}
                    webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                    print(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 195, 'svalue': data.get('timestamp')}
                webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                #print(url + urllib.parse.urlencode(getVars))
        #inverter values
                inverters = data.get('inverters')
        #count number of inverters
                Inverter_qty = len(data.get('inverters'))
                print('Number inverter: ' + str(Inverter_qty))
        # loop trough all inverters and get the data
                for i in range(Inverter_qty):
                    Inverter = list(inverters.keys())[i]
                    print('Inverter Id: ' + Inverter)
                    InverterOnline = data['inverters'][Inverter]['online']
                    print('Online: ' + str(InverterOnline))
                    InverterFrequency = data['inverters'][Inverter]['frequency']
                    print('Frequency: ' + str(InverterFrequency) + ' Hz')
                    InverterSignal = data['inverters'][Inverter]['signal']
                    print('Signal: ' + str(InverterSignal) + ' %')
                    InverterTemperature = data['inverters'][Inverter]['temperature']
                    print('Temperature: ' + str(InverterTemperature) + ' °C')
                    nPower = len(data['inverters'][Inverter]['power'])
                    nVoltage = len(data['inverters'][Inverter]['voltage'])
                    voltage = data['inverters'][Inverter]['voltage'][0]
                    print('Voltage inverter ' + str(i + 1) + ' panel ' + str(1) + ': ' + str(voltage) + ' V') 
                    for x in range(nPower):
                        power = data['inverters'][Inverter]['power'][x]
                        print('Power inverter ' + str(i + 1) + ' panel ' + str(x + 1) + ': ' + str(power) + ' W')

        #upload values to Domoticz for inverter 1
                        if (i == 0) :
                            if (float(InverterTemperature) > 0):
                                getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 174, 'svalue': InverterTemperature}
                                webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            if (float(InverterFrequency) > 0):
                                getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 69, 'svalue': InverterFrequency}
                                webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 70, 'svalue': InverterSignal}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            if (float(voltage) > 0):   
                                getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 71, 'svalue': (voltage)}
                                webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        if (Inverter_qty == 1):
                            if InverterOnline == True :
                                getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': 3, 'switchcmd': 'On'}
                            else :
                                getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': 3, 'switchcmd': 'Off'}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
 
        #upload values to Domoticz for inverter 2
                        if (i == 1) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 179, 'svalue': InverterTemperature}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 212, 'svalue': InverterFrequency}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 213, 'svalue': InverterSignal}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 214, 'svalue': (voltage)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        if (Inverter_qty == 2):
                            if InverterOnline == True :
                                getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': 180, 'switchcmd': 'On'}
                            else :
                                getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': 180, 'switchcmd': 'Off'}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))

        #upload power values to Domoticz for inverter 1
                        if (i == 0) and (x == 0) :  
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 196, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 0) and (x == 1) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 197, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 0) and (x == 2) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 198, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 0) and (x == 3) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 199, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
 
        #upload power values to Domoticz for inverter 2
                        if (i == 1) and (x == 0) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 200, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 1) and (x == 1) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 201, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 1) and (x == 2) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 202, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 1) and (x == 3) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 203, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
 
        except Exception as err:
            print(f"[ERROR]", {err})
 
        #print(f"Sleeping for {sleep} sec")
        time.sleep(sleep)
