#!/usr/bin/env python3
 
from APSystemsECUR import APSystemsECUR
import time
import asyncio
import urllib.request
import urllib.parse
import urllib
from pprint import pprint
 
 
ecu_ip = "WiFi IP ECU-R"
#Communication delay to ECU (sec)
sleep = 300
 
url = 'http://IP-Domoticz:8080/json.htm?'
puntcomma = '\u003B'
 
loop = asyncio.get_event_loop()
ecu = APSystemsECUR(ecu_ip)
 
while True:
        try:
                data = loop.run_until_complete(ecu.async_query_ecu())
                #pprint(data)
 
                lifetime_energy = str(data.get('lifetime_energy')*1000)
                today_energy_kwh = str(data.get('today_energy')*1000)
                current_power = str(data.get('current_power'))
                print('current_power: ' + current_power)
                generated_energy = (current_power + puntcomma + lifetime_energy)
                print('output: ' + today_energy_kwh + ';' + current_power)
                #pwr = .format(today_energy_kwh, current_power)
                #print('PWR: ' + pwr)
                print('Today energy [kWh]: ' + today_energy_kwh)
                if (float(today_energy_kwh) >= 0 or float(current_power) >= 0):
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
                print('Inverter_cnt: ' + str(Inverter_qty))
        # loop trough all inverters and get the data
                for i in range(Inverter_qty):
                    Inverter = list(inverters.keys())[i]
                    print('InverterId: ' + Inverter)
                    InverterOnline = data['inverters'][Inverter]['online']
                    print('Online: ' + str(InverterOnline))
                    InverterFrequency = data['inverters'][Inverter]['frequency']
                    print('Frequency: ' + str(InverterFrequency))
                    InverterSignal = data['inverters'][Inverter]['signal']
                    print('Signal: ' + str(InverterSignal))
                    InverterTemperature = data['inverters'][Inverter]['temperature']
                    print('Temperature: ' + str(InverterTemperature))
                    nPower = len(data['inverters'][Inverter]['power'])
                    nVoltage = len(data['inverters'][Inverter]['voltage'])
                    voltage = data['inverters'][Inverter]['voltage'][0]
                    print('Voltage inverter ' + str(i + 1) + ' panel ' + str(1) + ': ' + str(voltage) + ' V') 
                    for x in range(nPower):
                        power = data['inverters'][Inverter]['power'][x]
                        print('Power inverter ' + str(i + 1) + ' panel ' + str(x + 1) + ': ' + str(power) + ' W')

        #upload values to Domoticz voor inverter 1
                        if (i == 0) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 174, 'svalue': InverterTemperature}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 69, 'svalue': InverterFrequency}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 70, 'svalue': InverterSignal}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 71, 'svalue': (voltage)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        if InverterOnline == True :
                            getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': 175, 'switchcmd': 'On', 'level': 0, 'passcode': '' }
                        else :
                            getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': 175, 'switchcmd': 'Off', 'level': 0, 'passcode': '' }
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
 
        #upload values to Domoticz voor inverter 2
                        if (i == 1) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 179, 'svalue': InverterTemperature}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 212, 'svalue': InverterFrequency}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 213, 'svalue': InverterSignal}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 214, 'svalue': (voltage)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        if InverterOnline == True :
                            getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': 180, 'switchcmd': 'On', 'level': 0, 'passcode': '' }
                        else :
                            getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': 180, 'switchcmd': 'Off', 'level': 0, 'passcode': '' }
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
 
        #upload values to Domoticz voor inverter 3
                        if (i == 2) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 185, 'svalue': InverterTemperature}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 215, 'svalue': InverterFrequency}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 216, 'svalue': InverterSignal}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 217, 'svalue': (voltage)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        if InverterOnline == True :
                            getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': 186, 'switchcmd': 'On', 'level': 0, 'passcode': '' }
                        else :
                            getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': 186, 'switchcmd': 'Off', 'level': 0, 'passcode': '' }
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
 
        #upload values to Domoticz voor inverter 4
                        if (i == 3) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 191, 'svalue': InverterTemperature}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 218, 'svalue': InverterFrequency}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 219, 'svalue': InverterSignal}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 220, 'svalue': (voltage)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        if InverterOnline == True :
                            getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': 192, 'switchcmd': 'On', 'level': 0, 'passcode': '' }
                        else :
                            getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': 192, 'switchcmd': 'Off', 'level': 0, 'passcode': '' }
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
 
        #upload power values to Domoticz voor inverter 1
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
 
        #upload power values to Domoticz voor inverter 2
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
 
        #upload power values to Domoticz voor inverter 3
                        if (i == 2) and (x == 0) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 204, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 2) and (x == 1) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 205, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 2) and (x == 2) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 206, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 2) and (x == 3) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 207, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
 
        #upload power values to Domoticz voor inverter 4
                        if (i == 3) and (x == 0) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 208, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 3) and (x == 1) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 209, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 3) and (x == 2) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 210, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
                        elif (i == 3) and (x == 3) :
                            getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': 211, 'svalue': (power)}
                            webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
 
 
        except Exception as err:
            print(f"[ERROR]", {err})
 
        #print(f"Sleeping for {sleep} sec")
        time.sleep(sleep)