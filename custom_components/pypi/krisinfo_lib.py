import logging
import json
import aiohttp
from urllib.request import urlopen
from math import radians, sin, cos, acos

_LOGGER = logging.getLogger(__name__)

class KrisInformation():

    # initialize with all props
    def __init__(
            self, id: str, push_message: str, updated: str,
            published: str, headline: str, preamble: str,
            body_text: str, web: str, language: str,
            event: str, sender_name: str, source_id: str,
            area: array, links: array) -> None:
        """Constructor"""
        self._id = id
        self._push_message = push_message
        self._updated = updated
        self._published = published
        self._headline = headline
        self._preamble = preamble
        self._body_text = body_text
        self._web = web
        self._language = language
        self._event = event
        self._sender_name = sender_name
        self._source_id = source_id
        self._area = area
        self._links = links

    @property
    def id(self) -> str:
        """string id of the message"""
        return self._id

    @property
    def push_message(self) -> str:
        """push_message of the message"""
        return self._push_message
    
    @property
    def updated(self) -> str:
        return self.self_updated

    @property
    def published(self) -> str:
        return self._published

    @property
    def headline(self) -> str:
        return self._headline
    
    @property
    def preamble(self) -> str:
        return self._preamble
    
    @property
    def body_text(self) -> str:
        return self._body_text
    
    @property
    def web(self) -> str:
        return self._web
    
    @property
    def language(self) -> str:
        return self._language
    
    @property
    def event(self) -> str:
        return self._event
    
    @property
    def sender_name(self) -> str:
        return self._sender_name

    @property
    def source_id(self) -> str:
        return self._source_id
    
    @property
    def area(self) -> array:
        return self._area
    
    @property
    def links(self) -> array:
        return self._links


class KrisInformationAPI:
    """Get the latest data and update the states."""

    def __init__(self, longitude, latitude, radius):
        """Initialize the data object."""
        
        self.slat = latitude
        self.slon = longitude
        self.radius = radius
        self.attributes = {}
        self.attributes["messages"] = []
        self.data = {}
        self.available = True
        self.update()
        self.data['state'] = "No new messages"

    @Throttle(SCAN_INTERVAL)
    def update(self):
        """Get the latest data from Krisinformation."""
        try:
            _LOGGER.debug("Trying to update")
            response = urlopen('https://api.krisinformation.se/v2/feed?format=json')
            data = response.read().decode('utf-8')
            jsondata = json.loads(data)

            self.data['state'] = "No new messages"
            self.attributes["messages"] = []
            for index, element in enumerate(jsondata):
                self.make_object(index = index, element = element)
            
            self.data['attributes'] = self.attributes
            self.available = True
        except Exception as e:
            _LOGGER.error("Unable to fetch data from Krisinformation.")
            _LOGGER.error(str(e))
            self.available = False
            
    def make_object(self, index, element):
        message = {}
        message['Area'] = []
        
        distance = None
        within_range = False
        
        for count, area in enumerate(element['Area']):
            message['Area'].append({ "Type" : area['Type'], "Description" : area['Description'], "Coordinate" : area['Coordinate']})
            distance = self.calculate_distance(coords = area['Coordinate'])
            if float(distance) < float(self.radius):
                within_range = True
        
        if within_range:
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
            for numbers, link in enumerate(element['BodyLinks']):
                message['Links'].append(link['Url'])
            message['SourceID'] = element['SourceID']
            # _LOGGER.error(message)
            
            self.attributes["messages"].append(message)
            if element['Event'] == "Alert":
                self.state = "Alert"
            else:
                self.state = "News"
            self.data['state'] = self.state
            
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


class KrisInformation():
    def __init__(self, longitude: str, latitude: str, radius: str,
                 session: aiohttp.ClientSession = None,
                 api: KrisInformationAPI()) -> None:
        self._longitude = str(round(float(longitude), 6))
        self._latitude = str(round(float(latitude), 6))
        self.radius = radius
        self._api = api

        if session:
            self._api.session = session

    def get_messages(self)