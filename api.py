import json
from urlparse import urlparse
import httplib2 as http     # External library


<<<<<<< HEAD
class Api(object):
=======
class api(object):
>>>>>>> 56a3c28479e5cfa126af0cdf3c905cf778866315
    '''
ID: int
Name: string
Transport Type: string
API Link: string
Method: string
API Key: dict
'''
    def __init__(self, ID, Name, TransportType, APILink, Method, APIKey):
<<<<<<< HEAD
        super(Api, self).__init__()
=======
        super(api, self).__init__()
>>>>>>> 56a3c28479e5cfa126af0cdf3c905cf778866315
        self.ID = ID
        self.Name = Name
        self.TransportType = TransportType
        self.APILink = APILink
        self.Method = Method
        self.APIKey = APIKey

    def getTransportType(self):
        return self.TransportType

    def getAPILink(self):
        return self.APILink

    def getAPIKey(self, getFirst=True):
        if getFirst is True:
            return self.APIKey[1]
        return self.APIKey

    def getMethod(self):
        return self.Method

    def callAPI(self, **kwargs):
        if self.TransportType == 'Taxi':
            return self.callTaxiAPI(self)
        if self.TransportType == 'Bus':
            return self.callBusAPI(self, kwargs['Bustop'])

        pass

    def callTaxiAPI(self):
        if(self.TransportType == 'Taxi'):
            # From DataMall Document
            headers = {'AccountKey': '8LOiGaQeTXO97oC7KkSYHA==', 'accept': 'application/json'}  # this is by default
            # API parameters
            uri = 'http://datamall2.mytransport.sg/'  # Resource URL
            path = 'ltaodataservice/Taxi-Availability?'
            # Build query string & specify type of API call
            target = urlparse(uri + path)
            method = 'GET'
            body = ''
            # Get handle to http
            h = http.Http()
            # Obtain results
            response, content = h.request(target.geturl(), method, body, headers)
            # Parse JSON to print
            jsonObj = json.loads(content)
            return json.dumps(jsonObj, sort_keys=True, indent=4)
        else:
            print "Error: Wrong Type API Call"

    def callBusAPI(self, Bustop):
        if(self.TransportType == 'Bus'):
            # From DataMall Document
            headers = {'AccountKey': '8LOiGaQeTXO97oC7KkSYHA==', 'accept': 'application/json'}  # this is by default
            # API parameters
            uri = 'http://datamall2.mytransport.sg/'  # Resource URL
            path = 'ltaodataservice/BusArrivalv2?'
            request = 'BusStopCode='
            # Build query string & specify type of API call
            target = urlparse(uri + path + request + Bustop)
            method = 'GET'
            body = ''
            # Get handle to http
            h = http.Http()
            # Obtain results
            response, content = h.request(target.geturl(), method, body, headers)
            # Parse JSON to print
            jsonObj = json.loads(content)
            return json.dumps(jsonObj, sort_keys=True, indent=4)
        else:
            print "Error: Wrong Type API Call"
