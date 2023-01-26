#!/usr/bin/env python3
 
from APSystemsECU import APSystemsECU
import time
import asyncio
import urllib.request
import urllib.parse
import urllib
from pprint import pprint
 
#START USER CONFIGURATION

#Change your ECU IP
ecu_ip = "IP ECU-B"

#Change your Domoticz IP
url = 'http://IP-Domoticz:8080/json.htm?'

#Change your idx
SolarGeneration = 175
SwitchInverter1 = 178
SwitchInverter2 = 180
ConsumptionInverter1Pannel1 = 196
ConsumptionInverter1Pannel2 = 197
ConsumptionInverter1Pannel3 = 198
ConsumptionInverter1Pannel4 = 199
ConsumptionInverter2Pannel1 = 200
ConsumptionInverter2Pannel2 = 201
TemperatureInverter1 = 177
TemperatureInverter2 = 179
Timestamp = 176
SignalInverter1 = 210
SignalInverter2 = 213
VoltageInverter1 = 211
VoltageInverter2 = 214
FrequencyInverter1 = 212
FrequencyInverter2 = 215

#END USER CONFIGURATION

#Communication delay to ECU (sec)
sleep = 300 

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
                    getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': SolarGeneration, 'svalue': (generated_energy)}
                    webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                    print(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': Timestamp, 'svalue': data.get('timestamp')}
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
                        if (i == 0) and (x == 0) :  
                            if (float(InverterTemperature) > 0):
                                getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': TemperatureInverter1, 'svalue': InverterTemperature}
                                webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            if (float(InverterFrequency) > 0):
                                getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': FrequencyInverter1, 'svalue': InverterFrequency}
                                webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': SignalInverter1, 'svalue': InverterSignal}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            if (float(voltage) > 0):   
                                getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': VoltageInverter1, 'svalue': (voltage)}
                                webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                            if InverterOnline == True :
                                getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': SwitchInverter1, 'switchcmd': 'On'}
                            else :
                                getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': SwitchInverter1, 'switchcmd': 'Off'}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter1Pannel1, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 0) and (x == 1) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter1Pannel2, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 0) and (x == 2) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter1Pannel3, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 0) and (x == 3) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter1Pannel4, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
 
        #upload values to Domoticz for inverter 2
                        if (i == 1) and (x == 0) :
                            if (float(InverterTemperature) > 0):
                                getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': TemperatureInverter2, 'svalue': InverterTemperature}
                                webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            if (float(InverterFrequency) > 0):
                                getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': FrequencyInverter2, 'svalue': InverterFrequency}
                                webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': SignalInverter2, 'svalue': InverterSignal}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            if (float(voltage) > 0):   
                                getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': VoltageInverter2, 'svalue': (voltage)}
                                webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                            if InverterOnline == True :
                                getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': SwitchInverter2, 'switchcmd': 'On'}
                            else :
                                getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': SwitchInverter2, 'switchcmd': 'Off'}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter2Pannel1, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 1) and (x == 1) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter2Pannel2, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
 
        except Exception as err:
            print(f"[ERROR]", {err})
 
        #print(f"Sleeping for {sleep} sec")
        time.sleep(sleep)
