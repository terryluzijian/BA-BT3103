import json
from BasicAPI import BasicAPI


def lambda_handler(event, context):
    building = InterbuildingAPI(event['lat'], event['lon'])
    return building.get_connected_buildings_nearby()


class InterbuildingAPI(BasicAPI):

    type_name = 'interbuilding'
    building_connection = json.load(open('data/BUILDING_CONNECTION.json', 'r'))
    building_geocode = json.load(open('data/BUILDING_GEOCODE.json', 'r'))
    building_distance = json.load(open('data/BUILDING_DISTANCE.json', 'r'))
    building_shortest_path_matrix = json.load(open('data/BUILDING_SHORTEST_PATH_MATRIX.json', 'r'))

    def __init__(self, user_lat, user_lon, search_distance=BasicAPI.proximity_threshold):
        super(InterbuildingAPI, self).__init__(user_lat, user_lon, search_distance)
        self.buildings = []
        self.buildings_nearby = []
        self.search_distance = search_distance
        self.get_buildings()
        self.get_buildings_nearby()

    def get_buildings(self):
        self.buildings.extend([{
            'index': i,
            'lat': self.building_geocode[i]['lat'],
            'lon': self.building_geocode[i]['lon'],
            'name': self.building_geocode[i]['name']
        } for i in range(len(self.building_geocode))])

    def get_buildings_nearby(self):
        if self.buildings == []:
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
        self.buildings_nearby = buildings_nearby

    def get_connected_buildings_nearby(self):  # Only return as [{index of nearby_building: [index of its connected buildings ]}]
        if self.buildings_nearby == []:    # need to call index_to_building(index) to return the building object
            self.get_buildings_nearby()
        nearest_building = self.buildings_nearby[0]
        connected_buildings_nearby = sorted([{nearest_building['index']:self.get_connected_buildings(nearest_building['index'])}])[0]
        return {'buildings': {'search_distance': self.search_distance,
                              'results': [list(map(self.index_to_building, i)) for i in map(lambda x: self.building_shortest_path_matrix[connected_buildings_nearby.keys()[0]][x]['path'], connected_buildings_nearby.values()[0])]}}

    def get_building_connection_nearby(self):
        pass

    def get_connected_buildings(self, building_index):
        return [i for i in range(len(self.building_shortest_path_matrix[building_index])) if self.building_shortest_path_matrix[building_index][i] != {}]

    def get_interbuilding_path(self, start_building_index, goal_building_index):  # Only return as [Paths of buildings]
        if self.building_shortest_path_matrix[start_building_index][goal_building_index] != []:
            return {'nodes': self.building_shortest_path_matrix[start_building_index][goal_building_index]['nodes'],
                    'dist': self.building_shortest_path_matrix[start_building_index][goal_building_index]['total_cost'],
                    'edges': self.building_shortest_path_matrix[start_building_index][goal_building_index]['edges']
                    }

        else:
            return []

    def index_to_building(self, index):
        if self.buildings == []:
            self.get_buildings()
        return [building for building in self.buildings if building['index'] == index][0]

    def _bfs(self, graph, start):
        visited, queue = set(), [start]
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                queue.extend(set([i for i in range(len(graph[vertex])) if graph[vertex][i] == 1]) - visited)
        return list(visited)


'''  Old Version
    def get_connected_buildings_nearby(self):  # Only return as [{index of nearby_building: [index of its connected buildings ]}]
        if self.buildings_nearby == []:    # need to call index_to_building(index) to return the building object
            self.get_buildings_nearby()
        connected_buildings_nearby = [{building_dict['index']:[buildings
                                                               for buildings in self._bfs(self.building_connection, building_dict['index'])
                                                               ]} for building_dict in self.buildings_nearby]
        return connected_buildings_nearby

    def get_interbuilding_path(self, start_building_index, goal_building_index):  # Only return as [Paths of buildings]
        if self.buildings == []:                                                  # need to call index_to_building(index) to return the building object
            self.get_buildings()
        interbuilding_path_index = self._dfs_paths(self.building_connection, start_building_index, goal_building_index)
        return interbuilding_path_index

    def _bfs(self, graph, start):
        visited, queue = set(), [start]
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                queue.extend(set([i for i in range(len(graph[vertex])) if graph[vertex][i] == 1]) - visited)
        return list(visited)

    def _dfs_paths(self, graph, start, goal):
        if goal in self._bfs(graph, start):
            stack = [(start, [start])]
            result = []
            while stack:
                if len(result) >= 3:  # Limit on possible paths results as 3
                    break
                (vertex, path) = stack.pop()
                for next in set([i for i in range(len(graph[vertex])) if graph[vertex][i] == 1]) - set(path):
                    if next == goal:
                        result.append(path + [next])
                    else:
                        stack.append((next, path + [next]))
            return result
        else:
            return []

    def _bfs_paths(self, graph, start, goal):
        if goal in self._bfs(graph, start):
            queue = [(start, [start])]
            result = []
            while queue:
                if len(result) >= 3:  # Limit on possible paths results as 3
                    break
                (vertex, path) = queue.pop(0)
                for n in (set([i for i in range(len(graph[vertex])) if graph[vertex][i] == 1]) - set(path)):
                    if n == goal:
                        result.append(path + [n])
                    else:
                        queue.append((n, path + [n]))
            return result
        else:
            return []

    def index_to_building(self, index):
        if self.buildings == []:
            self.get_buildings()
        return [building for building in self.buildings if building['index'] == index]
'''
