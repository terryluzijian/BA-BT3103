import boto.dynamodb
import datetime
import json
from scripts.BikeAPI import BikeAPI
from scripts.BusAPI import BusAPI
from scripts.TaxiAPI import TaxiAPI

key_dict = {key: value for sub_dict in json.load(open('data/AWS_KEY.json', 'r')) for key, value in sub_dict.items()}

conn = boto.dynamodb.connect_to_region('ap-southeast-1',
                                       aws_access_key_id=key_dict['aws_access_key_id'],
                                       aws_secret_access_key=key_dict['aws_secret_access_key'])
table = conn.get_table('PublicTransport')


def api_integrate_handler(event, context):

    test_geo = (1.296644, 103.776587)  # Center
    range_in_km = 1.5

    # Get bikes
    test_geos = [  # Points around
        (1.296644, 103.776587),
        (1.298355, 103.776896), (1.295969, 103.779632), (1.293991, 103.776819), (1.296221, 103.773947),
        (1.298879, 103.774374), (1.296532, 103.782949), (1.293118, 103.782406), (1.292102, 103.777217),
        (1.293558, 103.772105), (1.296440, 103.771355), (1.302750, 103.773720), (1.305411, 103.773087)
    ]

    bike_result_concat = []
    for test_geo in test_geos:
        bike_api = BikeAPI(test_geo[0], test_geo[1], search_distance=0.5)
        bike_result_concat.extend(bike_api.get_bike_result()['bike'])

    bike_final_result_concat = []
    bike_coord_set = set()
    for bike_dict in bike_result_concat:
        if (bike_dict['brand'], bike_dict['lat'], bike_dict['lon']) not in bike_coord_set:
            bike_coord_set.add((bike_dict['brand'], bike_dict['lat'], bike_dict['lon']))
            bike_final_result_concat.append({
                'brand': bike_dict['brand'],
                'code': bike_dict['code'],
                'dist': BikeAPI.get_distance((bike_dict['lat'], bike_dict['lon']), test_geo),
                'lat': bike_dict['lat'],
                'lon': bike_dict['lon'],
                'type': bike_dict['type']
            })

    bike_final_result_concat = sorted(bike_final_result_concat, key=lambda new_bike_dict: new_bike_dict['dist'])

    # Get taxi and bus
    taxi_api = TaxiAPI(test_geo[0], test_geo[1], range_in_km)
    bus_api = BusAPI(test_geo[0], test_geo[1], range_in_km)
    taxi_final_result = taxi_api.get_taxi_result()['taxi']
    bus_final_result = bus_api.get_bus_result()['bus']

    final_list = bike_final_result_concat + taxi_final_result + bus_final_result
    for final_dict in final_list:
        final_dict.update({'timestamp': str(datetime.datetime.utcnow() + datetime.timedelta(hours=8))})
        final_dict.update({'key': '%s %s %s' % (final_dict['type'], final_dict['brand'], final_dict['code'])})

    for item in final_list:
        table_item = table.new_item(hash_key=item['key'],
                                    range_key=item['timestamp'],
                                    attrs={
                                        key: value for key, value in item.items() if key not in ['key', 'timestamp']
                                        })
        table_item.put()
