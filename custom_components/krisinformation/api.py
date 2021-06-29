import logging
import json

from math import radians, sin, cos, acos
from custom_components.krisinfo.kriscom import kriscom

from .const import (
    INTEGRATION_DOMAIN,
    INTEGRATION_ATTRIBUTION,
    INTEGRATION_EVENTS
)

class KrisinformationAPI:
    """Get the latest data and update the states."""

    def __init__(self, hass, longitude, latitude, county, radius, country):
        """Initialize the data object."""
        
        self.hass = hass
        self.logger = logging.getLogger(INTEGRATION_DOMAIN)
        self.slat = latitude
        self.slon = longitude
        self.county = county
        self.radius = radius
        self.country = country
        self.attributes = {}
        self.attributes["messages"] = []
        self.attributes["news_count"] = 0
        self.attributes["alert_count"] = 0
        self.attributes["total_count"] = 0
        self.attributes["filtered_count"] = 0
        self.attributes["display_state"] = "No new messages"
        self.attributes["display_icon"] = "mdi:check-circle-outline"
        self.attributes["attribution"] = INTEGRATION_ATTRIBUTION
        self.data = {}
        self.available = True
        self.update()
        self.data['state'] = 0

    async def getDiag(self):
        return {
            'available': self.available,
            'count': self.attributes["total_count"],
            'filtered': self.attributes["filtered_count"],
        }

    async def update(self):
        """Get the latest data from Krisinformation."""
        #try:
        self.logger.debug("Trying to update")
        communicator = kriscom()
        response = await communicator.request()

        oldNews = self.attributes["news_count"]
        oldAlerts = self.attributes["alert_count"]

        self.data['state'] = 0
        self.attributes["messages"] = []
        self.attributes["news_count"] = 0
        self.attributes["alert_count"] = 0
        self.attributes["total_count"] = 0
        self.attributes["filtered_count"] = 0
        self.attributes["display_state"] = "No new messages"
        self.attributes["display_icon"] = "mdi:check-circle-outline"

        for index, element in enumerate(response):
            self.attributes["filtered_count"] =+ 1
            self.make_object(index = index, element = element)
        
        if (self.attributes["news_count"]>0):
            self.attributes["display_state"] = f"{self.attributes['news_count']} News Messages"
            self.attributes["display_icon"] = "mdi:alert-circle-outline"                

        if (self.attributes["alert_count"]>0):
            self.attributes["display_state"] = f"{self.attributes['alert_count']} Alert Messages"
            self.attributes["display_icon"] = "mdi:alert-circle"                

        self.data['state'] = self.attributes["total_count"]
        self.data['attributes'] = self.attributes
        self.available = True

        if self.attributes["news_count"]>oldNews:
            self.hass.bus.fire(INTEGRATION_EVENTS, {"event_type": "news_avaliable"})

        if self.attributes["alert_count"]>oldAlerts:
            self.hass.bus.fire(INTEGRATION_EVENTS, {"event_type": "alerts_avaliable"})

        self.hass.bus.fire(INTEGRATION_EVENTS, {"event_type": "refresh_completed"})
        #except Exception as e:
        #    self.hass.bus.fire(INTEGRATION_EVENTS, {"event_type": "refresh_error", "error": str(e)})
        #    self.logger.error("Unable to fetch data from Krisinformation.")
        #    self.logger.error(str(e))
        #    self.available = False
            
    def make_object(self, index, element):
        message = {}
        message['Area'] = []
        
        distance = None
        within_range = False
        is_in_county = False
        is_in_country = False
        
        for count, area in enumerate(element['Area']):
            message['Area'].append({ "Type" : area['Type'], "Description" : area['Description'], "Coordinate" : area['Coordinate']})
            
            if self.country is not None:
                if area['Type'] == 'Country':
                    if self.country.lower() in area['Description'].lower():
                        is_in_country = True
                
            else:
                if self.county is not None:
                    if area['Type'] == 'County':
                        if self.county.lower() in area['Description'].lower():
                            is_in_county = True
                    
                distance = self.calculate_distance(coords = area['Coordinate'])
                if float(distance) < float(self.radius):
                    within_range = True
        
        if within_range or is_in_county or is_in_country:
            message['ID'] = element['Identifier']
            message['Message'] = element['PushMessage']
            message['Updated'] = element['Updated']
            message['Published'] = element['Published']
            message['Headline'] = element['Headline']
            message['Preamble'] = element['Preamble']
            message['BodyText'] = element['BodyText']
            message['Web'] = element['Web']
            message['Language'] = element['Language']
            message['Event'] = element['Event']
            message['SenderName'] = element['SenderName']
            message['Links'] = []
            if element['BodyLinks'] is not None:
                for numbers, link in enumerate(element['BodyLinks']):
                    message['Links'].append(link['Url'])
            message['SourceID'] = element['SourceID']
            
            self.attributes["messages"].append(message)

            if element['Event'] == "Alert":
                self.attributes["alert_count"] += 1
            else:
                self.attributes["news_count"] += 1
            self.attributes["total_count"] += 1
        else:
            self.attributes["filtered_count"] += 1

            
    def calculate_distance(self, coords):
        coords = coords.split()
        coords = coords[0].split(',')
        elon = coords[0]
        elat = coords[1]
        
        #Convert coordinates to radians
        elat2 = radians(float(elat))
        slat2 = radians(float(self.slat))
        elon2 = radians(float(elon))
        slon2 = radians(float(self.slon))
        
        #Calculate the distance between them
        dist = 6371.01 * acos(sin(slat2)*sin(elat2) + cos(slat2)*cos(elat2)*cos(slon2 - elon2))

        return dist
