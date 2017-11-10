import math


class BasicAPI(object):

    proximity_threshold = 0.3  # 300m

    def __init__(self, user_lat, user_lon):
        self.user_lat = user_lat
        self.user_lon = user_lon
        self.raw_response = {}

    def get_concat_result(self, keys, functions, type_name):
        raw_concat = []
        for key, this_function in zip(keys, functions):
            raw_concat.extend(this_function(self.raw_response[key])[type_name])
        return {
            type_name: raw_concat
        }

    @staticmethod
    def get_distance(point_a, point_b):
        # Copyright from author Wayne Dyck
        lat1, lon1 = point_a
        lat2, lon2 = point_b
        radius = 6371  # km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
                                                      * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(
            dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c
        return d
