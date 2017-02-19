#!/home/npseventsite/py/bin/python
print "Content-type: text/html"
print
print "<html><head><link rel='stylesheet' href='styles.css'></head><body>"
import sites
import events
import cgi
import datetime

import cgitb
cgitb.enable()

postData = cgi.FieldStorage()
dateReq = dateReq = datetime.datetime.combine(datetime.date.today(), datetime.time(0,0))
siteReq = "all"
DATA = {}

if postData.has_key('date'):
	dateStrArray = postData['date'].value.split("-")
	dateReq = datetime.datetime(int(dateStrArray[0]),int(dateStrArray[1]),int(dateStrArray[2]))
print '<p style="display:none">' + dateReq.isoformat("T") + '</p>'

exclusions = {}
if postData.has_key("exclude"):
	for ex in postData["exclude"].value.split(","):
		exclusions[ex] = True
inclusions = {}
if postData.has_key('include'):
	for incl in postData["include"].value.split(","):
		inclusions[incl] = True
#else:
	#inclusions = False

if postData.has_key('site'):
	siteReq = postData['site'].value.split(",")
	DATA['sites'] = sites.getData(siteReq,dateReq)['sites']
	keywords = []
	for s in DATA['sites']:
		for k in s['keywords']:
			keywords.append(k)
		for l in s['locations']:
			keywords.append(l)
	if (not exclusions.has_key("events")) and (not inclusions) or (inclusions.has_key("events")):
		DATA['events'] = events.getData(keywords,dateReq)['events']
else:
	DATA['sites'] = sites.getData(["all"],dateReq)['sites']
	if (not exclusions.has_key("events")) and (not inclusions) or (inclusions.has_key("events")):
		DATA['events'] = events.getData(['all'],dateReq)['events']

for site in DATA['sites']:
	print "<div>"
	if (not exclusions.has_key("name")) and (not inclusions) or (inclusions.has_key("name")):
		print "<h1>" + site['name'] + "</h1>"
	if (not exclusions.has_key("hours")) and (not inclusions) or (inclusions.has_key("hours")):
		print '<div><img src="https://www.nps.gov/bost/planyourvisit/images/hours.png">'
		print "<h3 class='listing'>Today&apos;s hours: " + site["hours"] + "</h3></div>"
	if (site["fees_required"]) and (not exclusions.has_key("fees")) and (not inclusions) or (inclusions.has_key("fees")):
		print "<div>"
		if site["fees_required"] == "true":
			print '<img src="https://www.nps.gov/bost/planyourvisit/images/fee.png">'
		else:
			if(site["fees_required"] == "false"):
				print '<img src="https://www.nps.gov/bost/planyourvisit/images/non-fee.png">'
		print "<ul class='listing'>"
		for fee in site["fees"]:
			print "<li style='list'>%s</li>" % fee
		print "</ul>"	
		print "</div>"
	if len(site["accessibility"]) > 0 and (not exclusions.has_key("accessibility")) and (not inclusions) or (inclusions.has_key("accessibility")):
		for consideration in site["accessibility"]:
			print "<div>"
			if consideration["accessible"] == "true":
				print '<img src="https://www.nps.gov/bost/planyourvisit/images/accessible.png">'
			else:
				if(consideration["accessible"] == "false"):
					print '<img src="https://www.nps.gov/bost/planyourvisit/images/not-accessible.png">'
			print "<span class='listing'>" + consideration["consideration"] + "</span>"
			print "</div>"

	if len(site["websites"]) > 0 and (not exclusions.has_key("websites")) and (not inclusions) or (inclusions.has_key("websites")):
		print '<div><img src="https://www.nps.gov/bost/planyourvisit/images/www.png">'
		print "<ul class='listing'>"
		for website in site["websites"]:
			print "<li><a href='%s' target='_blank'>%s</a></li>" % (website["href"], website["text"])
		print '</ul>'
		print '</div>'
	if DATA.has_key("events"):
		for event in DATA['events']:
			if event['location'] in site['keywords'] or event['location'] in site['locations']:
				print "<h3>%s</h3>" %event['title'].encode('utf-8')
				print "<h5>%(formattedStartTime)s%(formattedEndTime)s - %(location)s</h5>" %{'location':event['location'].encode('utf-8'),'formattedStartTime':event['formattedStartTime'].encode('utf-8'),'formattedEndTime':event['formattedEndTime'].encode('utf-8')}
				print "<p>" + event['content'].encode('utf-8') + "</p>"
	print "</div>"
	print "<hr>"
print "</body></html>"