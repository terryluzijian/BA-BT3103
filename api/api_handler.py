from scripts.BikeAPI import BikeAPI
from scripts.BusAPI import BusAPI
from scripts.TaxiAPI import TaxiAPI


def bus_api_handler(event, context):
    # User geographical coordinates
    user_geo = {
        'lat': event['lat'],
        'lon': event['lon']
    }

    # Initialize API
    bus_api = BusAPI(user_lat=user_geo['lat'], user_lon=user_geo['lon'])

    # Fetch result
    bus_result = bus_api.get_bus_result()

    return {
        'bus':
            {
                'search_distance': bus_api.search_distance,
                'results': bus_result['bus']
            },
    }


def taxi_api_handler(event, context):
    # User geographical coordinates
    user_geo = {
        'lat': event['lat'],
        'lon': event['lon']
    }

    # Initialize API
    taxi_api = TaxiAPI(user_lat=user_geo['lat'], user_lon=user_geo['lon'])

    # Fetch result
    taxi_result = taxi_api.get_taxi_result()

    return {
        'taxi':
            {
                'search_distance': taxi_api.search_distance,
                'results': taxi_result['taxi']
            }
    }


def bike_api_handler(event, context):
    # User geographical coordinates
    user_geo = {
        'lat': event['lat'],
        'lon': event['lon']
    }

    # Initialize API
    bike_api = BikeAPI(user_lat=user_geo['lat'], user_lon=user_geo['lon'])

    # Fetch result
    bike_result = bike_api.get_bike_result()

    return {
        'bike':
            {
                'search_distance': bike_api.search_distance,
                'results': bike_result['bike']
            },
    }


def integrate_api_handler(event, context):
    # User geographical coordinates
    user_geo = {
        'lat': event['lat'],
        'lon': event['lon']
    }

    # Initialize API
    bike_api = BikeAPI(user_lat=user_geo['lat'], user_lon=user_geo['lon'])
    bus_api = BusAPI(user_lat=user_geo['lat'], user_lon=user_geo['lon'])
    taxi_api = TaxiAPI(user_lat=user_geo['lat'], user_lon=user_geo['lon'])

    # Fetch result
    bike_result = bike_api.get_bike_result()
    bus_result = bus_api.get_bus_result()
    taxi_result = taxi_api.get_taxi_result()

    return \
        {
            'bike':
                {
                    'search_distance': bike_api.search_distance,
                    'results': bike_result['bike']
                },
            'bus':
                {
                    'search_distance': bus_api.search_distance,
                    'results': bus_result['bus']
                },
            'taxi':
                {
                    'search_distance': taxi_api.search_distance,
                    'results': taxi_result['taxi']
                }
        }
