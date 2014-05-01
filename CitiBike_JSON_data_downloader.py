import urllib2
import csv
import json
from pprint import pprint

site1= 'http://api.citybik.es/citibikenyc.json'
site2= 'http://citibikenyc.com/stations/json'
site3=''#local text file
#json_data=urllib2.urlopen(site2)#.read()

json_data=open(site2).read()

data = json.load(json_data)
pprint(data)
json_data.close()

new_csv = ''#destination
c_out = open(new_csv,'wb')
cw=csv.writer(c_out, dialect='excel')

site2List=['time','altitude', 'availableBikes', 'availableDocks', 'city', 'id', 'landMark', 'lastCommunicationTime','latitude', 'location', 'longitude', 'postalCode','stAddress1', 'stAddress2','stationName','statusKey', 'statusValue', 'testStation', 'totalDocks']
site1List=['name','idx','timestamp', 'number', 'free', 'bikes', 'coordinates', 'address', 'lat', 'lng', 'id']


#site2Data=[i['altitude'],i['availableBikes'],i['availableDocks'],i['city'],i['id'],i['landMark'],i['lastCommunicationTime'],i['latitude'],i['location'],i['longitude'],i['postalCode'],i['stAddress1'],i['stAddress2'],i['stationName'],i['statusKey'],i['statusValue'],i['testStation'],i['totalDocks']]
#site1Data= [i['name'],i['idx'], i['timestamp'], i['number'], i['free'], i['bikes'], i['coordinates'], i['address'], i['lat'], i['lng'], i['id']]
cw.writerow(site2List)

for i in data['stationBeanList']:
    site2Data=[data['executionTime'],i['altitude'],i['availableBikes'],i['availableDocks'],i['city'],i['id'],i['landMark'],i['lastCommunicationTime'],i['latitude'],i['location'],i['longitude'],i['postalCode'],i['stAddress1'],i['stAddress2'],i['stationName'],i['statusKey'],i['statusValue'],i['testStation'],i['totalDocks']]
    cw.writerow(site2Data)

c_out.close()
