# National Parks of Boston Today at the Park API

##A framework for retrieving, *creating (TODO)* and posting events, hours, closure notices and basic visiting info for the parks and park partners of the National Parks of Boston

###Retrieving data

All requests are made as `GET` requests with different endpoints specifying the return format and different parameters to specify and manipulate the returned data.

####JSON return format

This format request should be used when the data will be further processed or manipulated in a client-side script or within an app.

#####Usage:
`GET https://bostonnpsevents.com/tap/json.cgi`

#####Default response (no parameters):
Returns a JSON object of all data relating to all sites, and all events scheduled for this current day.

#####Optional Parameters:
|Parameter Name		|Value											|Description													|
|-------------------|-----------									|-------------------											|
|site				|Any valid site abbreviation(s)comma separated	|Use to filter out results unrelated to the sites(s) requested.	|
|date				|Date in UTC format YYYY-MM-DD					|Use to request a specific date.								|

#####Example response with parameters:
`GET https://bostonnpsevents.com/tap/json.cgi?site=PRH,ONC&date=2017-04-18`

Response will be a JSON object of the site information and events for the Paul Revere House and Old North Church on the date April 18, 2017.

#####JSON data representation:
```javascript
{
	"date_requested" : "2017-04-18T00:00:00",
	"sites" : [{
			"abbr" : "PRH",
			"name" : "Paul Revere House",			
			"hours" : "Open 9:30 a.m. - 5:15 p.m.",
			"fees_required" : "true",
			"fees" : ["Adults: $5.00", "Seniors & Students: $4.50", "Ages 5-17: $1.00"],
			"accessibility" : [{
					"accessible" : "true",
					"consideration" : "The first floor of the house is accessible via the courtyard ramps. The second floor is accessible via the elevator in the visitor center and then taking the catwalk to the house."
				}
			],
			"keywords" : ["Paul Revere House", "North Square", "North Sq", "Hichborn House"],
			"locations" : ["Paul Revere House", "Paul Revere Garden", "Pierce Hitchborn House"],
			"websites" : [{
					"text" : "Visit the Paul Revere House website.",
					"href" : "http://www.paulreverehouse.org/"
				}
			],
		}, {
			"abbr" : "ONC",
			"name" : "Old North Church",
			"hours" : "Open 9 a.m. - 5 p.m.",
			"fees_required" : "true",
			"fees" : ["Admission by donation."],
			"accessibility" : [{
					"accessible" : "true",
					"consideration" : "Old North's sanctuary is accessible. <em>Note: To avoid steps in the courtyard while following the Freedom Trail from downtown, you will have to make a left at Unity St., take the right on to Tileston St., then make a right on to Salem St.</em>"
				}
			],
			"keywords" : ["Old North", "Salem St", "Salem Street", "Clough House"],
			"locations" : ["Old North Church", "Old North Campus", "Clough House - Old North Campus"],
			"websites" : [{
					"text" : "Visit the Old North website.",
					"href" : "http://oldnorth.com/"
				}
			],
		}
	],
	"events" : [{
			"title" : "Paul Revere House Self-Paced Tours",
			"content" : "Explore 18th-century family life at the home of the patriot silversmith.",
			"formattedStartTime" : "All Day",
			"formattedEndTime" : "",
			"allDay" : true,
			"location" : "Paul Revere House",
			"eventEndTime" : "2017-04-19",
			"eventStartTime" : "2017-04-18",
			"image" : "",
			"throwAway" : true
		}
	]
}
```
######Main object
|Property Name		|Value						|Description													|
|-------------------|-----------				|-------------------											|
|date_requested		|date string				|The date of the data returned in UTC format.					|
|sites				|array of site object(s)	|See table below												|
|events				|array of event object(s)	|See table below												|

######Sites object
|Property Name		|Value								|Description													|
|-------------------|-----------						|-------------------											|
|abbr				|string								|abbreviation of the site										|
|name				|string								|full name of the site											|
|hours				|string								|Written out hours of the site for the date returned			|
|fees_required		|string representation of boolean	|Boolean of whether there is a fee schedule or not.				|
|fees				|array of strings					|Each entry is a string describing an element of the fee schedule.|
|accessibility		|array of consideration objects		|See table below.|
|keywords			|array of strings					|Each entry is a string of a keyword used to link events to the site.|
|locations			|array of strings					|Each entry is a string of a sub-location or alternate name within the overall site.|
|websites			|array of website objects			|See table below.|

######Events object
|Property Name		|Value								|Description													|
|-------------------|-----------						|-------------------											|
|title				|string								|Name of the event.										|
|content			|string								|Description of the event.											|
|formattedStartTime	|string								|Written out starting time of the event, can be "All day" for all day events.|
|formattedEndTime	|string								|Written out ending time of the event, or null if all day.|
|allDay				|string representation of boolean	|Boolean of whether the event is an all day event.				|
|location			|string								|Location of the event.		|
|eventEndTime		|date string						|Start time in UTC format.|
|eventStartTime		|date string						|End time in UTC format.|
|image				|string URI							|URI pointing to an uploaded event image, or null if none.|
|throwAway			|string representation of boolean	|Boolean of whether the event is a less important recurring instance (for prioritizing on space-limited publications).|

######Consideration object
|Property Name		|Value						|Description													|
|-------------------|-----------				|-------------------											|
|accessible			|string representation of boolean	|Whether the consideration is accessible or not.		|
|consideration		|string								|Description of the consideration regarding accessibility.|

######Website object
|Property Name		|Value						|Description													|
|-------------------|-----------				|-------------------											|
|text				|string						|Text facing the user describing the hyperlink.					|
|href				|string	of url				|URL that an anchor tag would link to in its href property.		|


####HTML return format

This format returns data automatically formatted into a full html document. This is useful for iframe referencing in maps popups or info boxes, etc.

#####Usage:
`GET https://bostonnpsevents.com/tap/html.cgi`

#####Default response (no parameters):
Returns an HTML document of all sites with information and related events for the current day.

#####Optional Parameters:
|Parameter Name		|Value											|Description													|
|-------------------|-----------									|-------------------											|
|site				|Any valid site abbreviation(s)comma separated	|Use to filter out results unrelated to the sites(s) requested.	|
|date				|Date in UTC format YYYY-MM-DD					|Use to request a specific date.								|
|include			|Any valid properties listed below, comma separated					|Use to include specific properties in the page. If used, all unlisted properties are excluded.				|
|exclude			|Any valid properties listed below, comma separated					|Use to exclude specific properties from the page. If used all unlisted properties are included.			|

#####Include/Exclude properties list:

|Property Name		|
|------------------|
|name				|
|house				|
|events				|
|fees				|
|accessibility		|
|websites		|

#####Example response with parameters:
`GET https://bostonnpsevents.com/tap/html.cgi?site=PRH&date=2017-04-18&include=name,hours,events`

This example will return an HTML page for Paul Revere House with just the site's name, the hours of the day requested (April 18, 2017), and the events for that day and nothing else.



####JavaScript HTML injection

This format returns a snippet of JavaScript code that self-executes at load time to inject site and event data immediately following wherever a `<script>` tag is inserted in a webpage.
This is very useful for injecting dynamic content into static CMS pages, etc.

#####Usage:
In theory this is the HTTP command:

`GET https://bostonnpsevents.com/tap/script.cgi`

In actual usage, this is how the command is to be handled in a webpage:

`<script src='https://bostonnpsevents.com/tap/script.cgi'></script>`

#####Default response (no parameters):
Returns a JavaScript function and immediate call of that function which will insert HTML describing all sites and related events for the current day.

#####Optional Parameters:
|Parameter Name		|Value											|Description													|
|-------------------|-----------									|-------------------											|
|site				|Any valid site abbreviation(s)comma separated	|Use to filter out results unrelated to the sites(s) requested.	|
|date				|Date in UTC format YYYY-MM-DD					|Use to request a specific date.								|
|include			|Any valid properties listed below, comma separated					|Use to include specific properties in the page. If used, all unlisted properties are excluded.				|
|exclude			|Any valid properties listed below, comma separated					|Use to exclude specific properties from the page. If used all unlisted properties are included.			|
|string				|A custom string with handlbar property substitution |Use this to avoid the default HTML formatting and instead return a custom string. Useful for inline injection of hours, fees, etc.|

#####Include/Exclude/String properties list:

|Property Name		|
|------------------|
|name				|
|house				|
|events				|
|fees				|
|accessibility		|
|websites		|

#####Example response with include/exclude parameters:

TODO!!! Not fully functional *yet*

`<script src='https://bostonnpsevents.com/tap/html.cgi?site=PRH&date=2017-04-18&include=name,hours,events'></script>`

This example will inject HTML immediately following the `<script></script>` tags for Paul Revere House with just the site's name, the hours of the day requested (April 18, 2017), and the events for that day and nothing else.
The HTML formatting follows the same convention and styling as the HTML return format above.

#####Example response using custom string with handlebars:
