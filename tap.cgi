#!/home/npseventsite/py/bin/python
print "Content-type: text/json"
print
import sites
import events
import cgi
import datetime
import json
import cgitb
cgitb.enable()

postData = cgi.FieldStorage()
dateReq = dateReq = datetime.datetime.combine(datetime.date.today(), datetime.time(0,0))
siteReq = "all"
DATA = {}

if postData.has_key('date'):
	dateStrArray = postData['date'].value.split("-")
	dateReq = datetime.datetime(int(dateStrArray[0]),int(dateStrArray[1]),int(dateStrArray[2]))
DATA['date_requested'] = dateReq.isoformat("T")
if postData.has_key('site'):
	siteReq = postData['site'].value.split(",")
	DATA['sites'] = sites.getData(siteReq,dateReq)['sites']
	keywords = []
	for s in DATA['sites']:
		for k in s['keywords']:
			keywords.append(k)
		for l in s['locations']:
			keywords.append(l)
	DATA['events'] = events.getData(keywords,dateReq)['events']
else:
	DATA['sites'] = sites.getData(["all"],dateReq)['sites']
	DATA['events'] = events.getData(['all'],dateReq)['events']

print json.dumps(DATA)