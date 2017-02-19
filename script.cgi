#!/home/npseventsite/py/bin/python
print "Content-type: application/javascript"
print
print "function getData() {"
print "var self = document.currentScript;"

import sites
import events
import cgi
import datetime

import cgitb
cgitb.enable()

import urllib

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

postData = cgi.FieldStorage()
dateReq = dateReq = datetime.datetime.combine(datetime.date.today(), datetime.time(0,0))
siteReq = "all"
DATA = {}

if postData.has_key('date'):
	dateStrArray = postData['date'].value.split("-")
	dateReq = datetime.datetime(int(dateStrArray[0]),int(dateStrArray[1]),int(dateStrArray[2]))
print 'var date_requested = new Date("' + dateReq.isoformat("T") + '");'
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
exclusions = {}
inclusions = {}
if postData.has_key("exclude"):
	for ex in postData["exclude"].value.split(","):
		exclusions[ex] = True

if postData.has_key("string"):
	for site in DATA['sites']:
		string = postData["string"].value % site
		print "self.insertAdjacentHTML('afterend', decodeURIComponent('" +  urllib.quote(string) + "'));"
else:
	for site in DATA['sites']:
		siteString = ''
		if not exclusions.has_key('name'):
			siteString += "<div><h1>%s</h1>" % site["name"]
		if not exclusions.has_key("hours"):
			siteString +="<div><img src='https://www.nps.gov/bost/planyourvisit/images/hours.png' style='vertical-align: middle;'><h3 style='display:inline-block;list-style:none;padding-left:1em;vertical-align: middle;'>Today&apos;s hours: " + site["hours"] + "</h3></div>"
		if site["fees_required"] and not exclusions.has_key('fees'):
			siteString +="<div>"
			if site["fees_required"] == "true":
				siteString +='<img src="https://www.nps.gov/bost/planyourvisit/images/fee.png" style="vertical-align: middle;">'
			else:
				if(site["fees_required"] == "false"):
					siteString +='<img src="https://www.nps.gov/bost/planyourvisit/images/non-fee.png" style="vertical-align: middle;">'
			siteString +="<ul style='display:inline-block;list-style:none;padding-left:1em;vertical-align: middle;'>"
			for fee in site["fees"]:
				siteString +="<li style='list'>%s</li>" % fee
			siteString +="</ul></div>"
		if len(site["accessibility"]) > 0 and not (exclusions.has_key('accessibility')):
			for consideration in site["accessibility"]:
				siteString += "<div>"
				if consideration["accessible"] == "true":
					siteString += '<img src="https://www.nps.gov/bost/planyourvisit/images/accessible.png" style="vertical-align: middle;">'
				else:
					if(consideration["accessible"] == "false"):
						siteString += '<img src="https://www.nps.gov/bost/planyourvisit/images/not-accessible.png" style="vertical-align: middle;">'
				siteString += "<span style='display:inline-block;list-style:none;padding-left:1em;vertical-align: middle;'>" + consideration["consideration"] + "</span></div>"
		if len(site["websites"]) > 0 and not exclusions.has_key('websites'):
			siteString += '<div><img src="https://www.nps.gov/bost/planyourvisit/images/www.png" style="vertical-align: middle;">'
			for website in site["websites"]:
				siteString += "<a href='%s' target='_blank'>%s</a>" % (website["href"], website["text"])
			siteString += '</div>'
		siteString +="<hr></div>"
		print "self.insertAdjacentHTML('afterend', decodeURIComponent('" + urllib.quote(siteString) + "'));"
print "}"
print "getData();"