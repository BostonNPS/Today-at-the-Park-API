#!/usr/bin/python
#parses sites.xml and also looks for overriding hour data on gCal.
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime
import json

import xml.etree.ElementTree as ET
tree  = ET.parse('sites.xml')
sites = tree.getroot()

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = '/home/nps/.credentials/bostonnpsevents.json'
APPLICATION_NAME = 'Google Calendar CGI'
'''
def get_credentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,'calendar-python-cgi.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)
'''
'''
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
	creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))
'''

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=creds)

def getData(siteReq = ["all"], dateReq = datetime.datetime.combine(datetime.date.today(), datetime.time(0,0))):
	dateMax = dateReq + datetime.timedelta(1)
	if not isinstance(siteReq,list):
		siteReq = [siteReq]
	if siteReq[0] == "all":
		siteReq = ["all"]
	h = service.events().list(calendarId='7et3dj1eatj002e6485sqi5bu0@group.calendar.google.com', singleEvents=True, timeMin=dateReq.isoformat("T")+ "Z",timeMax=dateMax.isoformat("T")+ "Z").execute()
	siteData = []
	errors = []
	for sReq in siteReq:
		for site in sites:
			if(site.attrib['abbr'] == sReq) or siteReq[0] == 'all':
				currHours = ''
				for season in site.find("hours").findall("season"):
					try:
						if datetime.datetime.strptime(season.attrib["start"] + " " + str(dateReq.year),"%B %d %Y") <= dateReq <= datetime.datetime.strptime(season.attrib["end"] + " " + str(dateReq.year),"%B %d %Y"):
							currHours = season.find("default").text
							for exception in season.findall("exception"):
								#if there is an exception with attribute day (i.e. Sunday, Monday, etc.) only meaning every Sunday, Monday, etc...
								if exception.attrib.has_key('day') and not exception.attrib.has_key('nth') and exception.attrib['day'] == dateReq.strftime("%A"):
									currHours = exception.text
								#if there is an exception where it is the nth day (Sunday, Monday, etc.) and optionally a specific month stated...
								if exception.attrib.has_key('day') and exception.attrib.has_key('nth') and exception.attrib['day'] == dateReq.strftime("%A"):
									#first get the day (number in the month) the nth Sunday/Monday/etc. actually is
									lastday = ''
									nth = 0
									dateofnthday = ''
									if dateReq.month == 12:
										lastday = datetime.date(dateReq.year + 1, 1, 1) - datetime.timedelta (days = 1)
									else:
										lastday = datetime.date(dateReq.year, dateReq.month + 1, 1) - datetime.timedelta (days = 1)
									for x in range(1,lastday.day):
										if datetime.date(dateReq.year,dateReq.month,x).strftime("%A") == exception.attrib['day']:
											nth = nth + 1
											if nth == int(exception.attrib['nth']):
												dateofnthday = datetime.date(dateReq.year,dateReq.month,x)
									if ((not exception.attrib.has_key('month')) or (exception.attrib.has_key('month') and exception.attrib['month'] == dateReq.strftime("%B")) and dateofnthday.day == dateReq.day):
										currHours = exception.text
								#if there is an exception on an nth day AND a specific month...
								#if (exception.attrib.has_key('day') and exception.attrib.has_key('nth') and exception.attrib.has_key('month')) and (exception.attrib['day'] == dateReq.strftime("%A") and ((dateReq.day/7) + 1) == int(exception.attrib['nth'] and exception.attrib['month'] == dateReq.strftime("%B"))):
								#	currHours = exception.text
								#LASTLY if there is an explicit date specified (i.e. December 25.)
								if exception.attrib.has_key('date') and (dateReq.strftime("%B ") + str(dateReq.day) == exception.attrib['date'] or dateReq.strftime("%B %d") == exception.attrib['date']):
									currHours = exception.text
							for override in h['items']:
								startDate = ''
								if override['start'].has_key('date'):
									startDate = override['start']['date']
								else:
									if override['start'].has_key('dateTime'):
										startDate = override['start']['dateTime'].split('T')[0]
								if ((override["summary"] == site.attrib["abbr"]) or (override["summary"] == site.attrib["name"])) and (startDate == dateReq.strftime("%Y-%m-%d")):
									currHours = override["description"]
					except ValueError:
						errors.append("Date error somewhere for site " + site.attrib['abbr'] + ". Comparison: " + str(season.attrib["start"]) + " <= " + str(dateReq) + " <= " + str(season.attrib["end"]) + "</p>")
				feeinfo = []
				feeRequired = ""
				if site.find("fees"):
					for fee in site.find("fees").findall("item"):
						feeinfo.append(fee.text)
					if site.find("fees").attrib.has_key("required"):
						feeRequired = site.find("fees").attrib["required"]
				keywords = []
				if site.find("keywords"):
					for keyword in site.find("keywords").findall("keyword"):
						keywords.append(keyword.text)
				locations = []
				if site.find("locations"):
					for location in site.find("locations").findall("location"):
						locations.append(location.text)
				accessibility = []
				if site.find("accessibility"):
					for consideration in site.find("accessibility").findall("consideration"):
						accessible = ""
						if consideration.attrib.has_key("accessible"):
							accessible = consideration.attrib["accessible"]
						accessibility.append({'accessible':accessible,'consideration':consideration.text})
				websites = []
				for web in site.findall("website"):
					websites.append({'href':web.attrib['href'],'text':web.text})
				siteData.append({'name':site.attrib['name'],'abbr':site.attrib['abbr'], 'hours':currHours, 'fees_required':feeRequired,'fees':feeinfo, 'keywords' : keywords, 'locations':locations, 'accessibility':accessibility, 'websites':websites})
	return {'sites':siteData,'errors':errors}
	
def getToday(siteReq = ["all"]):
	return getData(siteReq)
def getTomorrow(siteReq = ["all"]):
	return getData(siteReq,datetime.datetime.combine(datetime.date.today(), datetime.time(0,0))+datetime.timedelta(1))
def getAfterTomorrow(siteReq = ["all"]):
	return getData(siteReq,datetime.datetime.combine(datetime.date.today(), datetime.time(0,0))+datetime.timedelta(2))
def getUTCDate(siteReq = ["all"],UTC_date = ""):
	return getData(siteReq,datetime.datetime.strptime(UTC_date.split("T")[0] + "T00:00:00",'%Y-%m-%dT%H:%M:%S'))
