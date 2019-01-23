import json
from typing import List

import abc
from datetime import datetime

from urllib.request import urlopen
import aiohttp
from math import radians, sin, cos, acos
import logging

_LOGGER = logging.getLogger(__name__)

API_URL = 'https://api.krisinformation.se/v2/feed?format=json'

class KrisinformationException(Exception):
    """Exception thrown if failing to access API"""
    pass

class KrisinformationMessage():
    # initialize with all props
    def __init__(
            self, id: str, push_message: str, updated: str,
            published: str, headline: str, preamble: str,
            body_text: str, web: str, language: str,
            event: str, sender_name: str, source_id: str,
            area: List[dict], links: List[str]) -> None:
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
        return self._updated

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
    def area(self) -> List[dict]:
        return self._area

    @property
    def links(self) -> List[str]:
        return self._links


class KrisinformationAPIBase():
    """Baseclass."""
    @abc.abstractmethod
    def get_messages_api(self) -> {}:
        """Override this"""
        raise NotImplementedError(
            'users must define get_messages to use this base class')

    @abc.abstractmethod
    async def async_get_messages_api(self) -> {}:
        """Override this"""
        raise NotImplementedError(
            'users must define async_get_messages to use this base class')


# pylint: disable=R0903
class KrisinformationAPI(KrisinformationAPIBase):
    """Default implementation for Krisinformation API"""

    def __init__(self) -> None:
        """Init the API with or without session"""
        self.session = None

    def get_messages_api(self):
        """gets data from API"""
        api_url = API_URL
        response = urlopen(api_url)
        data = response.read().decode('utf-8')
        jsondata = json.loads(data)
        return jsondata

    async def async_get_messages_api(self):
        """gets data from API async"""
        api_url = API_URL
        if self.session is None:
            self.session = aiohttp.ClientSession()
        async with self.session.get(api_url) as response:
            if response.status != 200:
                raise KrisinformationException("Failed to access krisinformation API with status code {}".format(response.status))
            data = await response.text()
        return json.loads(data)

class Krisinformation():
    def __init__(self, longitude: str, latitude: str, radius: str,
                 session: aiohttp.ClientSession = None,
                 api: KrisinformationAPIBase = KrisinformationAPI()) -> None:
        self._longitude = str(round(float(longitude), 6))
        self._latitude = str(round(float(latitude), 6))
        self._radius = str(round(float(latitude), 6))
        self._api = api

        if session:
            self._api.session = session


    def get_messages(self) -> List[KrisinformationMessage]:
        """Returns a list of messages"""
        json_data = self._api.get_messages_api()
        return _get_messages(json_data, self._longitude, self._latitude, self._radius)

    async def async_get_messages(self) -> List[KrisinformationMessage]:
        """Returns a list of messages"""
        json_data = await self._api.async_get_messages_api()
        return _get_messages(json_data, self._longitude, self._latitude, self._radius)

def _get_messages(api_result: dict, longitude: str, latitude: str, radius: str) -> List[KrisinformationMessage]:
    """Converts results from API to KrisinformationMessage list"""
    messages = []

    for element in api_result:
        distance = None
        within_range = False
        areas = []

        for area in enumerate(element['Area']):
            areas.append({ "Type" : area['Type'], "Description" : area['Description'], "Coordinate" : area['Coordinate']})
            distance = _calculate_distance(longitude, latitude, coords = area['Coordinate'])
            if float(distance) < float(radius):
                within_range = True

        if within_range:
            id = element['Identifier']
            push_message = element['PushMessage']
            updated = element['Updated']
            published = element['Published']
            headline = element['Headline']
            preamble = element['Preamble']
            body_text = element['BodyText']
            web = element['Web']
            language = element['Language']
            event = element['Event']
            sender_name = element['SenderName']
            links = []
            for link in enumerate(element['BodyLinks']):
                links.append(link['Url'])
            source_id = element['SourceID']

            message = \
                KrisinformationMessage(id, push_message, updated, published,
                headline, preamble, body_text, web, language,
                event, sender_name, source_id, area, links)

            messages.append(message)
            
def _calculate_distance(longitude: str, latitude: str, coords):
    coords = coords.split()
    coords = coords[0].split(',')
    elon = coords[0]
    elat = coords[1]
    
    #Convert coordinates to radians
    elat2 = radians(float(elat))
    slat2 = radians(float(latitude))
    elon2 = radians(float(elon))
    slon2 = radians(float(longitude))
    
    #Calculate the distance between them
    dist = 6371.01 * acos(sin(slat2)*sin(elat2) + cos(slat2)*cos(elat2)*cos(slon2 - elon2))

    return dist