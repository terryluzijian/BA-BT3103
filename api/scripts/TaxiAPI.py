import requests
from .BasicAPI import BasicAPI


class TaxiAPI(BasicAPI):

    type_name = 'taxi'

    def __init__(self, user_lat, user_lon, search_distance=BasicAPI.proximity_threshold * 3):
        super(TaxiAPI, self).__init__(user_lat, user_lon, search_distance)
        self.raw_result = []
        self.get_taxi_response()

    def get_taxi_result(self):
        raw_processed = [
            {
                'lat': taxi_dict['Latitude'],
                'lon': taxi_dict['Longitude'],
                'dist': self.get_distance((self.user_lat, self.user_lon),
                                          (taxi_dict['Latitude'], taxi_dict['Longitude'])),
                'code': taxi_index,
                'brand': 'Public',
                'type': 'taxi'
            }
            for taxi_dict, taxi_index in zip(self.raw_result, range(len(self.raw_result)))
        ]
        return {
            self.type_name: sorted(filter(lambda taxi_dict: taxi_dict['dist'] <= self.search_distance,
                                          raw_processed), key=lambda new_taxi_dict: new_taxi_dict['dist'])
        }

    def get_taxi_response(self):
        headers = {
            'AccountKey': BasicAPI.api_key['Public Taxi/Bus']
        }
        result = []
        for response_call in range(10):
            taxi_response = requests.get('http://datamall2.mytransport.sg/ltaodataservice/Taxi-Availability',
                                         headers=headers, params={'$skip': response_call * 500})
            result.extend(taxi_response.json()['value'])
        self.raw_result = result
