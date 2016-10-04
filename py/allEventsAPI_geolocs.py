#!/usr/bin/python
# -*- coding: latin-1 -*-

#for unicode problems, don't work here:
#from __future__ import unicode_literals

import httplib, urllib, base64, json, ast, csv, codecs, time, subprocess, os

import sys
reload(sys)
sys.setdefaultencoding('utf8')


# Paris Ile-de-France France
# Strasbourg Alsace France
# Dublin Dublin Ireland
# Copenhagen


#imputs pour la requête
ville = 'Paris'
region = 'Ile-de-France'
pays = 'France'
#debut = '18-08-2016'
debut = time.strftime("%d-%m-%Y")
#fin = '18-08-2016'
fin = time.strftime("%d-%m-%Y")
categorie = 'Concert'


# API request
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '28af234bf506421494a9193ffee6b090',
}
params = urllib.urlencode({
    # Request parameters
    'city': ville,
    'state': region,
    'country': pays,
    'page': '0',
    'sdate': debut,
    'edate': fin,
    'category': categorie,
})
try:
    conn = httplib.HTTPSConnection('api.allevents.in')
    conn.request("POST", "/events/list/?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
except:
    pass


# Data processed from json to csv file
data = json.loads(data)['data']


# Add FB URL to data
for i in range(len(data)):
    dict = data[i]
    dict[u'fb_event_url'] = 'https://www.facebook.com/events/' + data[i][u'event_id'] + '/'


# Select useful data
for j in range(len(data)):
    data[j] = data[j][u'eventname'],data[j][u'location'],data[j][u'fb_event_url'],data[j][u'venue'][u'longitude'],data[j][u'venue'][u'latitude'],data[j][u'start_time_display']
data = [('eventname','location','fb_event_url','longitude','latitude','start_time_display')] + data


# Export to new csv datafile
myfile1 = open('%s.csv' % (ville + '_' + categorie + '_' + debut), 'a')
wr = csv.writer(myfile1, quoting=csv.QUOTE_ALL)
for k in range(len(data)):
    wr.writerow(data[k])

# Store data to maps folder
prevName = '%s.csv' % (ville + '_' + categorie + '_' + debut)
newName = 'maps/%s.csv' % (ville + '_' + categorie + '_' + debut)
os.rename(prevName,newName)

# Create curlCommand file with curl command that upload datafile to online carto account
myfile2 = open('curlCommand.sh', 'w')
myfile2.write('curl -v -F file=@/home/lucas/Documents/gigzrProject/maps/' + ville + '_' + categorie + '_' + debut + '.csv "https://ldlucasdosso.carto.com/api/v1/imports/?api_key=fc1d0cf1c7b6bc8bd84d9a74e2f73bd7312f3cf2"');
myfile2.close()

# Execute curlCommand in command line
subprocess.call('chmod +x curlCommand.sh | ./curlCommand.sh', shell=True)
