import json
from BasicAPI import BasicAPI


class InterbuildingAPI(BasicAPI):

    type_name = 'interbuilding'
    building_connection = json.load(open('./data/BUILDING_CONNECTION.json', 'r'))
    building_geocode = json.load(open('./data/BUILDING_GEOCODE.json', 'r'))

    def __init__(self, user_lat, user_lon, search_distance=BasicAPI.proximity_threshold):
        super(InterbuildingAPI, self).__init__(user_lat, user_lon, search_distance)
        self.buildings = []
        self.buildings_nearby = []
        self.get_buildings()
        self.get_buildings_nearby()

    def get_buildings(self):
        self.buildings.extend([{
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
                        map(lambda building_dict:
                            {
                                'lat': building_dict['lat'],
                                'lon': building_dict['lon'],
                                'name': building_dict['name'],
                                'index': building_dict['index'],
                                'dist': self.get_distance((self.user_lat, self.user_lon),
                                                          (building_dict['lat'], building_dict['lon']))
                            },
                            self.buildings))),
            key=lambda building_final_dict: building_final_dict['dist'])
        self.buildings_nearby = buildings_nearby[:5]

    def get_connected_buildings_nearby(self):
        if len(self.buildings_nearby) == 0:
            self.get_buildings_nearby()
        connected_buildings_nearby = [{building_dict['index']:[buildings
                                                               for buildings in self._bfs(self.building_connection, building_dict['index'])
                                                              ]} for building_dict in self.buildings_nearby]
        return connected_buildings_nearby
    
    def _bfs(self, graph, start):
        visited, queue = set(), [start]
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                queue.extend(set([i for i in range(len(graph[vertex])) if graph[vertex][i] == 1]) - visited)
        return visited
    