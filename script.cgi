#!/home/bostonnp/virtualenv/public__html_tap/3.6/bin/python
print("Content-type: application/javascript")
print()
print("function getData() {")
print("var self = document.currentScript;")

import sites
import events
import cgi
import datetime

import cgitb
cgitb.enable()

import urllib.parse
import pystache
def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

postData = cgi.FieldStorage()
dateReq = dateReq = datetime.datetime.combine(datetime.date.today(), datetime.time(0,0))
siteReq = "all"
DATA = {}

if "date" in postData:
	dateStrArray = postData['date'].value.split("-")
	dateReq = datetime.datetime(int(dateStrArray[0]),int(dateStrArray[1]),int(dateStrArray[2]))
print('var date_requested = new Date("' + dateReq.isoformat("T") + '");')
if "site" in postData:
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
if "exclude" in postData:
	for ex in postData["exclude"].value.split(","):
		exclusions[ex] = True

inclusions = {}
if "include" in postData:
	for incl in postData["include"].value.split(","):
		inclusions[incl] = True

if "string" in postData or "handlebar" in postData:
	if "string" in postData:
		for site in DATA['sites']:
			string = postData["string"].value % site
			print("self.insertAdjacentHTML('afterend', decodeURIComponent('" +  urllib.parse.quote(string) + "'));")
	else:
		for site in DATA['sites']:
			print ("self.insertAdjacentHTML('afterend', decodeURIComponent('" +  urllib.parse.quote(pystache.render(postData['handlebar'].value,site)) + "'));")
else:
	for site in DATA['sites']:
		siteString = ''
		if (not "name" in exclusions) and (not inclusions) or ("name" in inclusions):
			siteString += "<div><h1>%s</h1>" % site["name"]
		if not (not "hours" in exclusions) and (not inclusions) or ("hours" in inclusions):
			siteString +="<div><img src='https://www.nps.gov/bost/planyourvisit/images/hours.png' style='vertical-align: middle;'><h3 style='display:inline-block;list-style:none;padding-left:1em;vertical-align: middle;'>Today&apos;s hours: " + site["hours"] + "</h3></div>"
		if (site["fees_required"]) and (not "fees" in exclusions) and (not inclusions) or ("fees" in inclusions):
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
		if len(site["accessibility"]) > 0 and (not "accessibility" in exclusions) and (not inclusions) or ("accessibility" in inclusions):
			for consideration in site["accessibility"]:
				siteString += "<div>"
				if consideration["accessible"] == "true":
					siteString += '<img src="https://www.nps.gov/bost/planyourvisit/images/accessible.png" style="vertical-align: middle;">'
				else:
					if(consideration["accessible"] == "false"):
						siteString += '<img src="https://www.nps.gov/bost/planyourvisit/images/not-accessible.png" style="vertical-align: middle;">'
				siteString += "<span style='display:inline-block;list-style:none;padding-left:1em;vertical-align: middle;'>" + consideration["consideration"] + "</span></div>"
		if len(site["websites"]) > 0 and (not "websites" in exclusions) and (not inclusions) or ("websites" in inclusions):
			siteString += '<div><img src="https://www.nps.gov/bost/planyourvisit/images/www.png" style="vertical-align: middle;">'
			for website in site["websites"]:
				siteString += "<a href='%s' target='_blank'>%s</a>" % (website["href"], website["text"])
			siteString += '</div>'
		if "events" in DATA and ((not "events" in exclusions) and (not inclusions) or ("events" in inclusions)):
			numHits = 0
			for event in DATA['events']:
				if event['location'] in site['keywords'] or event['location'] in site['locations']:
					numHits += 1
					siteString += "<h3>%s</h3>" %event['title'].encode('utf-8')
					siteString += "<h5>%(formattedStartTime)s%(formattedEndTime)s - %(location)s</h5>" %{'location':event['location'].encode('utf-8'),'formattedStartTime':event['formattedStartTime'].encode('utf-8'),'formattedEndTime':event['formattedEndTime'].encode('utf-8')}
					siteString += "<p>" + str(event['content'].encode('utf-8')) + "</p>"
			if numHits == 0 and "noEmpty" in postData and postData['noEmpty'].value == 'true':
				#print 'EXCLUDING' + site["name"]
				continue
		siteString +="<hr></div>"
		print("self.insertAdjacentHTML('afterend', decodeURIComponent('" + urllib.parse.quote(siteString) + "'));")
print( "}")
print("getData();")
