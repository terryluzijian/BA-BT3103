import json
from BasicAPI import BasicAPI


class InterbuildingAPI(BasicAPI):

    type_name = 'interbuilding'
    building_connection = json.load(open('data/BUILDING_CONNECTION.json', 'r'))
    building_geocode = json.load(open('data/BUILDING_GEOCODE.json', 'r'))

    def __init__(self, user_lat, user_lon, search_distance=BasicAPI.proximity_threshold):
        super(InterbuildingAPI, self).__init__(user_lat, user_lon, search_distance)
        self.buildings = []
        self.buildings_nearby = []
        self.get_buildings()
        self.get_buildings_nearby()

    def get_buildings(self):
        self.buidlings.extend([{
            'index': i,
            'lat': self.building_geocode[i]['lat'],
            'lon': self.building_geocode[i]['lng'],
            'name': self.building_geocode[i]['name']
        } for i in range(len(self.building_geocode))])

    def get_buildings_nearby(self):
        if len(self.buildings) == 0:
            self.get_buildings()
        buildings_nearby = sorted(
            list(filter(lambda building_new_dict: building_new_dict['dist'] <= self.search_distance,
                        map(lambda building_dct:
                            {
                                'lat': building_dct['lat'],
                                'lon': building_dct['lon'],
                                'name': building_dct['name'],
                                'index': building_dct['index'],
                                'dist': self.get_distance((self.user_lat, self.user_lon),
                                                          (building_dct['lat'], building_dct['lon']))
                            },
                            self.buildings))),
            key=lambda building_final_dict: building_final_dict['dist'])
        self.buildings_nearby = buildings_nearby

    def get_connected_buildings_nearby(self):
        if len(self.buildings_nearby) == 0:
            self.get_buildings_nearby()
