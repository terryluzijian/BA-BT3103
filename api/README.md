# Third-party Application Programming Interfaces (APIs)
This page compiles the APIs used by the application, mainly public transport availability such as taxi, bus and bike in Singapore. Following examples are illustrated using <code>Python</code> code snippets.

- [Public Bus and Taxi API](https://github.com/terryluzijian/BA-BT3103/tree/master/api#public-bus-and-taxi-api)
- [Bike APIs](https://github.com/terryluzijian/BA-BT3103/tree/master/api#bike-apis)
- [NUS School Shuttle Bus API](https://github.com/terryluzijian/BA-BT3103/tree/master/api#nus-school-shuttle-bus-api)
- [Google Map API](https://github.com/terryluzijian/BA-BT3103/tree/master/api#google-map-api)

## Public Bus and Taxi API

### Datamall
Refer to the **[pdf document](http://mytransport.sg/content/dam/mytransport/DataMall_StaticData/LTA_DataMall_API_User_Guide.pdf)** on how to fetch public transport data from MyTransport. Information is provided by Land Transport Authority (LTA).

### Bus
Public bus arrival time and bus stop codes can be accessed through the following *GET* request with access key and two bus-related parameters:

```python
import requests

headers = {
   'AccountKey' : '8LOiGaQeTXO97oC7KkSYHA==' # API access key here
}
payload = {
    'BusStopCode': 83139,
    'ServiceNo': 15
}
# Arrival time
bus_response = requests.get('http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2', 
                            headers=headers, params=payload)
# Bus stop
bus_stop_response = requests.get('http://datamall2.mytransport.sg/ltaodataservice/BusStops', headers=headers)
```

### Taxi
Taxi avilability is fetched through *GET* request but only top 500 records will be returned. An extra <code>$skip</code> parameter can be passed to retrieve next 500 records. An example would be:

```python
import requests

headers = {
   'AccountKey' : '8LOiGaQeTXO97oC7KkSYHA=='
}
taxi_response = requests.get('http://datamall2.mytransport.sg/ltaodataservice/Taxi-Availability', 
                             headers=headers, params={'$skip': 0})
```

## Bike APIs

### Obike
For Obike, an API call is made by *GET* method. One can simply pass the longtitude and latitude as parameters to the API link. An example would be:

```python
import requests
payload = {
    'latitude': 1.290270,
    'longitude': 103.851959
}
bike_obike = requests.get("https://mobile.o.bike/api/v1/bike/list", params=payload)
```

### Mobike
For Mobike, use *POST* request to trigger the API call. A trick here is to append *Wechat* as *Referer Header* and pass longtitude and latitude as parameters as usual:

```python
import requests
headers = {
    "Referer": "https://servicewechat.com/"
}
payload = {
    'latitude': 1.290270,
    'longitude': 103.851959
}
bike_mobike = requests.request("POST", "https://mwx.mobike.com/mobike-api/rent/nearbyBikesInfo.do",
                               headers=headers, params=payload)
```

The API response seems to spatially cover a fairly small range.

### Ofo
For Ofo, a much more header content with more detailed parameters should be passed to the call using *POST* request. One should create a session to fetch the response:

```python
import requests
headers = {
    "host": "one.ofo.com",
    "connection": "keep-alive", 
    "accept":  "*/*",
    "user-agent": "ofoBike/1.1.9 (iPhone; iOS 11.0; Scale/3.00)",
    "accept-language": "ja-JP;q=1, en-JP;q=0.9, zh-Hant-JP;q=0.8, zh-Hans-JP;q=0.7, ko-JP;q=0.6, de-JP;q=0.5",
    "content-length": "839",
    "accept-encoding": "gzip, deflate"
}
payload = {
    "countryCode": "SG",
    "languageArea": "SG",
    "lanugageCode": "en",
    "lat": 1.288799407680145,
    "lng": 103.7796760123914,
    "scale": 3,
    "source": 1,
    "source-version": 50,
    "token": "3e9133f0-a27b-11e7-882a-5937e108b29a" # User token generated through mobile registration
}
session = requests.Session()
session.headers.update(headers)
response = session.post("https://one.ofo.com/nearbyofoCar", data=payload)
```

## NUS School Shuttle Bus API
NUS School Shuttle Bus API can be called by simply executing a *GET* request. One can either fecth a list of available bus stops or the Estimated Time of Arrival (ETA) of shuttle buses for a particular station with parameters passed:

```python
import requests
bus_stops = requests.get('https://nextbus.comfortdelgro.com.sg/eventservice.svc/BusStops')
payload = {
    'busstopname': 'PGP'
}
arrival_time = requests.get('https://nextbus.comfortdelgro.com.sg/eventservice.svc/Shuttleservice', params=payload)
```

## Google Map API
Google Map API can be useful sometimes to calculate metrics such as distance and ETA.

**API Key:** *AIzaSyC0BWtfMs9N_hOKzWmwJNnhlfkwrGyYu1U*
