import datetime
import json
import requests
from .BasicAPI import BasicAPI


class BusAPI(BasicAPI):

    type_name = 'bus'
    public_shuttle_station = json.load(open('data/PUBLIC_SHUTTLE_CROSS.json', 'r'))
    public_shuttle_station_dict = {key: value for sub_dict in public_shuttle_station for key, value in sub_dict.items()}

    def __init__(self, user_lat, user_lon, search_distance=BasicAPI.proximity_threshold):
        super(BusAPI, self).__init__(user_lat, user_lon, search_distance)
        self.bus_stops = []
        self.bus_stops_nearby = []
        self.get_shuttle_bus_stops()
        self.get_stops_nearby()

    def get_bus_result(self):
        raw_result = self.get_bus_result_raw()[self.type_name]
        name_dict = {}
        result_list = []
        for bus_stop_dict in raw_result:
            name = bus_stop_dict['name']
            if name not in name_dict.keys():
                name_dict[name] = bus_stop_dict
                result_list.append(bus_stop_dict)
            else:
                same_bus_stop_dict = name_dict[name]
                del result_list[result_list.index(same_bus_stop_dict)]
                pair = sorted((bus_stop_dict, same_bus_stop_dict), key=lambda bus_dict: bus_dict['type'])
                result_list.append({
                    'lat': pair[0]['lat'],
                    'lon': pair[0]['lon'],
                    'name': pair[0]['name'],
                    'code': '%s/%s' % (pair[0]['code'], pair[1]['code']),
                    'type': '%s/%s' % (pair[0]['type'], pair[1]['type']),
                    'brand': '%s/%s' % (pair[0]['brand'], pair[1]['brand']),
                    'dist': pair[0]['dist'],
                    'arrival': [pair[0]['arrival'][0], pair[1]['arrival'][0]]
                })
        return {
            self.type_name: result_list
        }

    def get_bus_result_raw(self):
        return {self.type_name: [
            {
                'lat': bus_dict['lat'],
                'lon': bus_dict['lon'],
                'name': bus_dict['name']
                if bus_dict['name'] not in self.public_shuttle_station_dict.keys()
                else self.public_shuttle_station_dict[bus_dict['name']][0],
                'code': bus_dict['code'],
                'type': bus_dict['type'],
                'brand': bus_dict['brand'],
                'dist': bus_dict['dist'],
                'arrival': [{
                    bus_dict['type']: self.get_shuttle_bus_data(bus_dict['code']) if bus_dict['type'] == 'shuttle bus'
                    else self.get_public_bus_data(bus_dict['code'])
                }]
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
                list(filter(lambda bus_new_dict: bus_new_dict['dist'] <= self.search_distance,
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
            try:
                diff = datetime.datetime.strptime(time_stamp, '%Y-%m-%dT%H:%M:%S+08:00') - datetime.datetime.now()
                diff = diff.total_seconds() / 60.0
                if diff >= 1:
                    return '%d' % int(diff)
                elif diff < 0:
                    return '-'
                else:
                    return 'Arr'
            except ValueError:
                return '-'

        headers = {
            'AccountKey': BasicAPI.api_key['Public Taxi/Bus']
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
