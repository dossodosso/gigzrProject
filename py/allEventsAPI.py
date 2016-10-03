#!/usr/bin/python


import httplib, urllib, base64, json, ast

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '28af234bf506421494a9193ffee6b090',
}

params = urllib.urlencode({
    # Request parameters
    'city': 'Paris',
    'state': 'Ile-De-France',
    'country': 'France',
    'page': '0',
    'sdate': '11-06-2016',
    'edate': '11-06-2016',
    'category': 'Concert',
})

try:
    conn = httplib.HTTPSConnection('api.allevents.in')
    conn.request("POST", "/events/list/?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
except:
    pass
    # except Exception as e:
    # print("[Errno {0}] {1}".format(e.errno, e.strerror))


data = json.loads(data)['data']

for i in range(len(data)):
    dict = data[i]
    dict[u'fb_event_url'] = 'https://www.facebook.com/events/' + data[i][u'event_id'] + '/'

print data
