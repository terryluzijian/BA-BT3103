import re
import requests
from lxml import html
from queue import Queue

# Currently only for Kent Ridge Station (CKRG)
# Prospectively scale up to Haw Par Villa Station (CHPV) and One North Station (CONH)


def mrt_api_handler(event, context):

    site_session = requests.session()
    request_header = {
        'Referer': 'http://trainarrivalweb.smrt.com.sg/default.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    site_request = site_session.get('http://trainarrivalweb.smrt.com.sg/default.aspx', headers=request_header)
    html_parsed = html.fromstring(str(site_request.content))
    view_state = html_parsed.xpath('//*[@id="__VIEWSTATE"]/@value')[0]

    form_data = {
        '__VIEWSTATE': view_state,
        '__VIEWSTATEGENERATOR': 'CA0B0334',
        'ddlStation': 'CKRG',
    }
    another_request = site_session.post('http://trainarrivalweb.smrt.com.sg/default.aspx', headers=request_header, data=form_data)
    final_html_parsed = html.fromstring(another_request.content)

    arrival = final_html_parsed.xpath('//td/text()')
    arrival_dict = {}
    arrival_queue = Queue()

    for element in arrival:
        if ('min' in element) | ('-' in element):
            try:
                arrival_queue.put(re.search(r'\d+', element).group())
            except AttributeError:
                arrival_queue.put('-')
        else:
            if ('To %s' % element) not in arrival_dict.keys():
                arrival_dict['To %s' % element] = []
            arrival_dict['To %s' % element].append(arrival_queue.get())

    return {'mrt': {'results': {'Kent Ridge Station (CC24)': [{key: value} for key, value in arrival_dict.items()]}}}
