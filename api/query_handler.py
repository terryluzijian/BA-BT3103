import boto.dynamodb2
import datetime
import json
from boto.dynamodb2.table import Table

key_dict = {key: value for sub_dict in json.load(open('data/AWS_KEY.json', 'r')) for key, value in sub_dict.items()}

conn = boto.dynamodb2.connect_to_region('ap-southeast-1',
                                        aws_access_key_id=key_dict['aws_access_key_id'],
                                        aws_secret_access_key=key_dict['aws_secret_access_key'])
table = Table('PublicTransport', connection=conn)
sg_time_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)


def traverse_bus_arrival(arrival_list):

    def get_time_info(time_lst):
        if time_lst[0] == 'Arr':
            return 1
        if time_lst[0] != '-':
            return int(time_lst[0])
        elif time_lst[1] != '-':
            try:
                return int(time_lst[1])
            except ValueError:
                return 1
        else:
            return '-'

    arrival_list = eval(arrival_list)
    average_dict = {}
    for dict_item in arrival_list:
        for dict_key in dict_item.keys():
            average_dict[dict_key] = []
            arrival_items = dict_item[dict_key]
            for arrival_item in arrival_items:
                for arrival_item_key in arrival_item.keys():
                    time_list = arrival_item[arrival_item_key]
                    if get_time_info(time_list) != '-':
                        average_dict[dict_key].append(get_time_info(time_list))
        average_dict[dict_key] = 0 if len(average_dict[dict_key]) == 0 else (sum(average_dict[dict_key])/len(average_dict[dict_key]))
    return average_dict


def handle_bus_stop(event, context):

    bus_arrival_list = []
    past_time_list = []

    for past_hour in range(1, 13):
        past_time_stamp = sg_time_now - datetime.timedelta(hours=past_hour)
        past = str(past_time_stamp)[:13]
        past_time_list.append('%d:00' % past_time_stamp.hour)
        this_item = table.query(key__eq=' '.join([event['type'], event['brand'], event['code']]), timestamp__beginswith=past,
                                limit=2)
        for item in this_item:
            bus_arrival_list.append(traverse_bus_arrival(item['arrival']))

    final_lst = bus_arrival_list[::-1]
    traverse_dict = {}

    if len(final_lst) > 0:
        for key in final_lst[0].keys():
            traverse_dict[key] = []
        for element in final_lst:
            for key in element.keys():
                traverse_dict[key].append(element[key])

    return {key: list(zip(past_time_list[::-1], value)) for key, value in traverse_dict.items()}


def handle_taxi_number(event, context):

    taxi_count = [0] * 12
    past_time_list = []
    for past_hour in range(1, 13):
        past_time_stamp = sg_time_now - datetime.timedelta(hours=past_hour)
        past = str(past_time_stamp)[:13]
        past_time_list.append('%d:00' % past_time_stamp.hour)
        this_item = table.scan(key__beginswith='taxi', timestamp__beginswith=past, type__eq='taxi')
        for item in this_item:
            taxi_count[past_hour - 1] += 1

    return list(zip(past_time_list[::-1], taxi_count[::-1]))


def handle_ofo_bike_number(event, context):

    bike_count = [0] * 12
    past_time_list = []
    for past_hour in range(1, 13):
        past_time_stamp = sg_time_now - datetime.timedelta(hours=past_hour)
        past = str(past_time_stamp)[:13]
        past_time_list.append('%d:00' % past_time_stamp.hour)
        this_item = table.scan(key__beginswith='bike', timestamp__beginswith=past, brand__eq='Ofo', type__eq='bike')
        for item in this_item:
            bike_count[past_hour - 1] += 1

    return list(zip(past_time_list[::-1], bike_count[::-1]))


def handle_bike_activity(event, context):

    usage = [0] * 12
    timestamp = []
    this_item = table.query(key__eq=' '.join([event['type'], event['brand'], event['code']]), limit=12)
    curr_index = 0
    curr_lat = 0
    curr_lon = 0
    for item in this_item:
        if curr_index != 0:
            if (item['lat'] != curr_lat) | (item['lon'] != curr_lon):
                if usage[curr_index - 1] != 0:
                    usage[curr_index] = usage[curr_index - 1] + 1
                else:
                    usage[curr_index] += 1
        curr_lat = item['lat']
        curr_lon = item['lon']
        timestamp.append([item['timestamp'], usage[curr_index]])
        curr_index += 1

    return timestamp[::-1]
