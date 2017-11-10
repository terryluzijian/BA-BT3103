import datetime
import json
import requests
from api.BasicAPI import BasicAPI


class BusAPI(BasicAPI):

    type_name = 'bus'

    def __init__(self, user_lat, user_lon):
        super(BusAPI, self).__init__(user_lat, user_lon)
        self.bus_stops = []
        self.bus_stops_nearby = []
        self.get_shuttle_bus_stops()
        self.get_stops_nearby()

    def get_bus_result(self):
        return {self.type_name: [
            {
                'lat': bus_dict['lat'],
                'lon': bus_dict['lon'],
                'name': bus_dict['name'],
                'code': bus_dict['code'],
                'type': bus_dict['type'],
                'brand': bus_dict['brand'],
                'dist': bus_dict['dist'],
                'arrival': self.get_shuttle_bus_data(bus_dict['code'])
                if bus_dict['type'] == 'shuttle bus' else self.get_public_bus_data(bus_dict['code'])
            } for bus_dict in self.bus_stops_nearby]}

    def get_stops_nearby(self):
        if len(self.bus_stops) > 0:
            public_bus_stops = json.load(open('data/PUBLIC_BUS_STOPS.json', 'r'))
            self.bus_stops.extend([{
                'lat': bus_dict['Latitude'],
                'lon': bus_dict['Longitude'],
                'name': bus_dict['Description'],
                'code': bus_dict['BusStopCode'],
                'type': 'public bus',
                'brand': 'Public'
            } for bus_dict in public_bus_stops])
            bus_stops_nearby = sorted(
                list(filter(lambda bus_new_dict: bus_new_dict['dist'] <= self.proximity_threshold,
                            map(lambda bus_dict:
                                {
                                    'lat': bus_dict['lat'],
                                    'lon': bus_dict['lon'],
                                    'name': bus_dict['name'],
                                    'code': bus_dict['code'],
                                    'type': bus_dict['type'],
                                    'brand': bus_dict['brand'],
                                    'dist': self.get_distance((self.user_lat, self.user_lon),
                                                              (bus_dict['lat'], bus_dict['lon']))
                                },
                                self.bus_stops))),
                key=lambda bus_final_dict: bus_final_dict['dist'])
            self.bus_stops_nearby = bus_stops_nearby

    def get_shuttle_bus_stops(self):
        bus_stops_response = requests.get('https://nextbus.comfortdelgro.com.sg/eventservice.svc/BusStops')
        if bus_stops_response.status_code == 404:
            self.bus_stops = self.bus_stops
        try:
            self.bus_stops.extend([{
                'lat': bus_dict['latitude'],
                'lon': bus_dict['longitude'],
                'name': bus_dict['caption'],
                'code': bus_dict['name'],
                'type': 'shuttle bus',
                'brand': 'NUS'
            } for bus_dict in bus_stops_response.json()['BusStopsResult']['busstops']])
        except KeyError:
            self.bus_stops = self.bus_stops

    @staticmethod
    def get_shuttle_bus_data(station_code):
        payload = {
            'busstopname': station_code
        }
        arrival_time = requests.get('https://nextbus.comfortdelgro.com.sg/eventservice.svc/Shuttleservice',
                                    params=payload)
        if arrival_time.status_code == 404:
            return []
        try:
            data = arrival_time.json()['ShuttleServiceResult']['shuttles']
        except KeyError:
            return []
        try:
            return [{sub_data['name']: [sub_data['arrivalTime'], sub_data['nextArrivalTime']]} for sub_data in data]
        except KeyError:
            return [{sub_data['name']: ['-', '-']} for sub_data in data]

    @staticmethod
    def get_public_bus_data(station_code):
        def get_approximate_mins(time_stamp):
            diff = ((datetime.datetime.strptime(time_stamp, '%Y-%m-%dT%H:%M:%S+08:00'))
                    - datetime.datetime.now()).total_seconds() / 60
            if diff >= 1:
                return '%d' % int(diff)
            elif diff < 0:
                return '-'
            else:
                return 'Arr'

        headers = {
            'AccountKey': '8LOiGaQeTXO97oC7KkSYHA=='
        }
        payload = {
            'BusStopCode': station_code,
        }
        bus_response = requests.get('http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2',
                                    headers=headers, params=payload)
        if bus_response.status_code == 404:
            return []
        try:
            data = bus_response.json()['Services']
        except KeyError:
            return []
        try:
            next_bus = [{bus_dict['ServiceNo']: [get_approximate_mins(bus_dict['NextBus']['EstimatedArrival'])]} for
                        bus_dict in data]
        except KeyError:
            next_bus = [{bus_dict['ServiceNo']: ['-', '-']} for bus_dict in data]
            return next_bus
        try:
            next_bus = [{bus_dict['ServiceNo']: [get_approximate_mins(bus_dict['NextBus']['EstimatedArrival']),
                                                 get_approximate_mins(bus_dict['NextBus2']['EstimatedArrival'])]}
                        for bus_dict in data]
            return next_bus
        except KeyError:
            return [{bus_dict['ServiceNo']: [get_approximate_mins(bus_dict['NextBus']['EstimatedArrival']), '-']} for
                    bus_dict in data]
