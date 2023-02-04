#!/usr/bin/env python3
 
from APSystemsECU import APSystemsECU
import time
import asyncio
import urllib.request
import urllib.parse
import urllib
from pprint import pprint
 
#////////// START USER CONFIGURATION \\\\\\\\\\

#Change your ECU IP
ecu_ip = "IP ECU"

#Change your Domoticz IP
url = 'http://IP-Domoticz:8080/json.htm?'

#Change your idx
Timestamp = 0
SolarGeneration = 0
SwitchInverter1 = 0
SwitchInverter2 = 0
SwitchInverter3 = 0
SwitchInverter4 = 0
ConsumptionInverter1Pannel1 = 0
ConsumptionInverter1Pannel2 = 0
ConsumptionInverter1Pannel3 = 0
ConsumptionInverter1Pannel4 = 0
ConsumptionInverter2Pannel1 = 0
ConsumptionInverter2Pannel2 = 0
ConsumptionInverter2Pannel3 = 0
ConsumptionInverter2Pannel4 = 0
ConsumptionInverter3Pannel1 = 0
ConsumptionInverter3Pannel2 = 0
ConsumptionInverter3Pannel3 = 0
ConsumptionInverter3Pannel4 = 0
ConsumptionInverter4Pannel1 = 0
ConsumptionInverter4Pannel2 = 0
ConsumptionInverter4Pannel3 = 0
ConsumptionInverter4Pannel4 = 0
TemperatureInverter1 = 0
TemperatureInverter2 = 0
TemperatureInverter3 = 0
TemperatureInverter4 = 0
SignalInverter1 = 0
SignalInverter2 = 0
SignalInverter3 = 0
SignalInverter4 = 0
VoltageInverter1 = 0
VoltageInverter2 = 0
VoltageInverter3 = 0
VoltageInverter4 = 0
FrequencyInverter1 = 0
FrequencyInverter2 = 0
FrequencyInverter3 = 0
FrequencyInverter4 = 0

#\\\\\\\\\\ END USER CONFIGURATION //////////

puntcomma = '\u003B'
loop = asyncio.get_event_loop()
ecu = APSystemsECU(ecu_ip)
 
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
getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': Timestamp, 'svalue': data.get('timestamp') + ' / ' + data.get('ecu_firmware')}
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
       elif (i == 1) and (x == 2) :
          getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter2Pannel3, 'svalue': (power)}
          webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
       elif (i == 1) and (x == 3) :
          getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter2Pannel4, 'svalue': (power)}
          webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
 
      #upload values to Domoticz for inverter 3
       if (i == 2) and (x == 0) :  
          if (float(InverterTemperature) > 0):
             getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': TemperatureInverter3, 'svalue': InverterTemperature}
             webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
          if (float(InverterFrequency) > 0):
             getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': FrequencyInverter3, 'svalue': InverterFrequency}
             webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
          getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': SignalInverter3, 'svalue': InverterSignal}
          webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
          if (float(voltage) > 0):   
             getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': VoltageInverter3, 'svalue': (voltage)}
             webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
          if InverterOnline == True :
             getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': SwitchInverter3, 'switchcmd': 'On'}
          else :
             getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': SwitchInverter3, 'switchcmd': 'Off'}
          webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
          getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter3Pannel1, 'svalue': (power)}
          webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
       elif (i == 2) and (x == 1) :
          getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter3Pannel2, 'svalue': (power)}
          webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
       elif (i == 2) and (x == 2) :
          getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter3Pannel3, 'svalue': (power)}
          webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
       elif (i == 2) and (x == 3) :
          getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter3Pannel4, 'svalue': (power)}
          webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')

      #upload values to Domoticz for inverter 4
       if (i == 3) and (x == 0) :  
          if (float(InverterTemperature) > 0):
             getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': TemperatureInverter4, 'svalue': InverterTemperature}
             webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
          if (float(InverterFrequency) > 0):
             getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': FrequencyInverter4, 'svalue': InverterFrequency}
             webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
          getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': SignalInverter4, 'svalue': InverterSignal}
          webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
          if (float(voltage) > 0):   
             getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': VoltageInverter4, 'svalue': (voltage)}
             webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
          if InverterOnline == True :
             getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': SwitchInverter4, 'switchcmd': 'On'}
          else :
             getVars = {'type' : 'command', 'param' : 'switchlight', 'idx': SwitchInverter4, 'switchcmd': 'Off'}
          webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars))
          getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter4Pannel1, 'svalue': (power)}
          webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
       elif (i == 3) and (x == 1) :
          getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter4Pannel2, 'svalue': (power)}
          webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
       elif (i == 3) and (x == 2) :
          getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter4Pannel3, 'svalue': (power)}
          webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
       elif (i == 3) and (x == 3) :
          getVars = {'type' : 'command', 'param' : 'udevice', 'nvalue' : 0, 'idx': ConsumptionInverter4Pannel4, 'svalue': (power)}
          webUrl = urllib.request.urlopen(url + urllib.parse.urlencode(getVars) + (puntcomma) + '0')
