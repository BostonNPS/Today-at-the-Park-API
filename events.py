#!/home/npseventsite/py/bin/python
#parses events found on the events gCal
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime
import json

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = '../../py/client_secret.json'
APPLICATION_NAME = 'Google Calendar CGI'

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

def getData(keywords = ["all"], dateReq = datetime.datetime.combine(datetime.date.today(), datetime.time(0,0))):
	dateMax = dateReq + datetime.timedelta(1)
	if not isinstance(keywords,list):
		keywords = [keywords]
	if keywords[0] == "all":
		keywords = ["all"]
	e = service.events().list(calendarId='vm30pfi0mudluethumg8f5kmrk@group.calendar.google.com', singleEvents=True, timeMin=dateReq.isoformat("T")+ "Z",timeMax=dateMax.isoformat("T")+ "Z").execute()
	EVENTS = []
	for event in e['items']:
		if event['location'] in keywords or keywords[0] == "all":
			#first, handle time, determine all day, etc.
			startTime = ''
			formatstart = ''
			endTime = ''
			formatend = ''
			allDay = ''
			throwAway = False
			if 'dateTime' in event['start']:
				startTime = event['start']['dateTime']
				startsplit = event['start']['dateTime'].split("T")[1].split(":")
				starthour = int(startsplit[0])
				if starthour > 12:
					starthour = starthour - 12
					if startsplit[1] == "00":
						formatstart = str(starthour) + " p.m. to "
					else:
						formatstart = str(starthour) + ":" + startsplit[1] + " p.m. to "
				elif starthour == 12:
					if startsplit[1] == "00":
							formatstart = "Noon to "
					else:
							formatstart = str(starthour) + ":" + startsplit[1] + " p.m. to "
				else:
					if startsplit[1] == "00":
							formatstart = str(starthour) + " a.m. to "
					else:
							formatstart = str(starthour) + ":" + startsplit[1] + " a.m. to "
				endTime = event['end']['dateTime']
				endsplit = event['end']['dateTime'].split("T")[1].split(":")
				endhour = int(endsplit[0])
				if endhour > 12:
					endhour = endhour - 12
					if endsplit[1] == "00":
							formatend = str(endhour) + " p.m."
					else:
							formatend = str(endhour) + ":" + endsplit[1] + " p.m."
				elif endhour == 12:
					if endsplit[1] == "00":
							formatend = "Noon"
					else:
							formatend = str(endhour) + ":" + endsplit[1] + " p.m."
				else:
					if endsplit[1] == "00":
							formatend = str(endhour) + " a.m."
					else:
							formatend = str(endhour) + ":" + endsplit[1] + " a.m."

				allDay = False
			else:
				startTime = event['start']['date']
				endTime = event['end']['date']
				formatstart = "All Day"
				allDay = True
			
			#check if asterisk at head of title. DEPRECATED. Use JSON key/value embedded in description.
			if event['summary'][0] == "*":
				throwAway = True
				event['summary'] = event['summary'].split("*")[1]
			
			#event description field section can hold json which can define imagery and other things. IF JSON, split out the keys as siblings of event content. if not, then keys are null and description field is handled as plain text.
			image = ''
			description = ''
			try:
				desc = json.loads(event['description'])
				if desc.has_key('image'):
					image = desc['image']
				if desc.has_key('description'):
					description = desc['description']
				if desc.has_key('priority'):
					throwAway = desc['priority']
			except ValueError:
				description = event['description']
				
			EVENTS.append({'title':event['summary'],'content':description,'image':image,'location':event['location'],'eventStartTime':startTime,'formattedStartTime':formatstart,'eventEndTime':endTime,'formattedEndTime':formatend,'allDay':allDay,'throwAway':throwAway})
	return {'date_requested':dateReq.isoformat("T"),'events':EVENTS}
def getToday(keywords = ["all"]):
	return getData(keywords)
def getTomorrow(keywords = ["all"]):
	return getData(keywords,datetime.datetime.combine(datetime.date.today(), datetime.time(0,0))+datetime.timedelta(1))
def getAfterTomorrow(keywords = ["all"]):
	return getData(keywords,datetime.datetime.combine(datetime.date.today(), datetime.time(0,0))+datetime.timedelta(2))
def getUTCDate(keywords = ["all"],UTC_date = ""):
	return getData(keywords,datetime.datetime.strptime(UTC_date.split("T")[0] + "T00:00:00",'%Y-%m-%dT%H:%M:%S'))
