import re
import requests


def mrt_api_handler(event, context):
    payload = {
        'stnCode': 'CKRG'
    }
    header = {
        'x-api-key': 'flQ0pqE76s7ZK1w2vhzVSNKkAAc8DK71aYmIuuW3'
    }
    response = requests.post('https://api.mrtapi.com/2.0/arrivals', params=payload, headers=header)
    content = eval(response.content)
    content_traversed = [[[final_value['nextTrainFinalDtn'], final_value['nextTrain']],
                         [final_value['subTrainFinalDtn'], final_value['subTrain']]]
                         for key, value in content.items()
                         for sub_key, sub_value in value.items()
                         for final_key, final_value in sub_value.items()]
    content_traversed = [sub_element for element in content_traversed for sub_element in element]
    content_traversed = list(map(lambda x: [x[0], re.sub(r'[^\d]', '', x[1])], content_traversed))
    content_traversed = list(filter(lambda y: len(' '.join(y[0].split())) > 1, content_traversed))

    final_content = {}
    for item_pair in content_traversed:
        if item_pair[0] not in final_content.keys():
            final_content[item_pair[0]] = []
        try:
            final_content[item_pair[0]].append(int(item_pair[1]))
        except ValueError:
            final_content[item_pair[0]].append('-')

    return {'mrt': {'CKRG': final_content}}
