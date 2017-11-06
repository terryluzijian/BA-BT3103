<<<<<<< HEAD
from scipy import spatial
import json

CampusStation = [{"name":"Aft Clementi Ave 1","stopID":"17091","latitude":"1.309051","longitude":"103.771483"},{ "name":"Aft Dover Road","stopID":"17099","latitude":"1.307979","longitude":"103.771676"},{ "name":"University Town","stopID":"19059","latitude":"1.308933","longitude":"103.772784"},{ "name":"New Town Sec Sch","stopID":"19051","latitude":"1.309073","longitude":"103.773846"},{ "name":"The Japanese Pr Sch","stopID":"16151","latitude":"1.300765","longitude":"103.769925"},{ "name":"NUS Fac Of Engrg","stopID":"16159","latitude":"1.300626","longitude":"103.770153"},{ "name":"NUS Raffles Hall","stopID":"16169","latitude":"1.300996","longitude":"103.772696"},{ "name":"Museum","stopID":"16161","latitude":"1.301050","longitude":"103.773715"},{ "name":"Opp Yusof Ishak Hse","stopID":"16179","latitude":"1.298990","longitude":"103.774176"},{ "name":"Yusof Ishak Hse","stopID":"16171","latitude":"1.298902","longitude":"103.774375"},{ "name":"Opp University Health Ctr","stopID":"18321","latitude":"1.298794","longitude":"103.775615"},{ "name":"University Health Ctr","stopID":"18329","latitude":"1.298928","longitude":"103.776114"},{ "name":"Blk S12","stopID":"18311","latitude":"1.297441","longitude":"103.777923"},{ "name":"Opp University Hall","stopID":"18319","latitude":"1.297530","longitude":"103.778131"},{ "name":"Lim Seng Tjoe Bldg (LT 27)","stopID":"18301","latitude":"1.297412","longitude":"103.781121"},{ "name":"Blk S17","stopID":"18309","latitude":"1.297522","longitude":"103.813380"},{ "name":"Opp NUH","stopID":"18239","latitude":"1.296790","longitude":"103.783191"},{ "name":"Nuh","stopID":"18221","latitude":"1.296303","longitude":"103.783411"},{ "name":"Kent Ridge Stn","stopID":"18331","latitude":"1.293707","longitude":"103.784890"},{ "name":"Opp Kent Ridge Stn","stopID":"18339","latitude":"1.293798","longitude":"103.785079"},{ "name":"Tentera Diraja Mque","stopID":"16141","latitude":"1.297889","longitude":"103.769599"},{ "name":"NUS Fac Of Achitecture","stopID":"16149","latitude":"1.297833","longitude":"103.769935"},{ "name":"Computer Ctr","stopID":"16189","latitude":"1.297515","longitude":"103.772819"},{ "name":"Ctrl Lib","stopID":"16181","latitude":"1.296604","longitude":"103.772519"},{ "name":"Opp Kent Ridge Ter","stopID":"16131","latitude":"1.294823","longitude":"103.769321"},{ "name":"Clementi Rd - Kent Ridge Ter","stopID":"16009","latitude":"1.294255","longitude":"103.769879"}]
CampusStation_parsed = [(station_dict['latitude'], station_dict['longitude']) for station_dict in CampusStation]


class PublicTransport(object):
=======
campusStation = []


class publicTransport(object):
>>>>>>> 56a3c28479e5cfa126af0cdf3c905cf778866315
    '''
ID: int
Type: string
Latitude: float
Longitude: float
Brand: string
Name: string
Current Nearest Station: string
Arrival Time to Stations: dict
    '''
<<<<<<< HEAD
    with open('CampusStation.json', 'r') as f:
        CampusStation = json.load(f)

=======
>>>>>>> 56a3c28479e5cfa126af0cdf3c905cf778866315
    def __init__(self, ID, Type, Latitude, Longitude, Brand, Name):
        self.ID = ID
        self.Type = Type
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.Brand = Brand
        self.Name = Name
        self.CurrentNearestStation = self.getCurrentNearestStation(self)
        self.ArrivalTimeToStations = self.getArrivalTime(self)

    def getLocation(self):
        return (self.Latitude, self.Longitude)

    def getType(self):
        return self.Type

    def getBrand(self):
        return self.Brand

    def getName(self):
        return self.Name

    def getArrivalTime(self):
<<<<<<< HEAD
        walkingSpeed = 3  # TODO: be changed into individual file
        return self.distance / walkingSpeed

    def getCurrentNearestStation(self):
        # CampusStation as JSON holding all campus stastion
        # Convert into CS as 2d array
        currentLocation = self.getLocation(self)
        self.distance, index = CampusStation_parsed[spatial.KDTree(CampusStation_parsed).query(currentLocation)[1]]
        CampusStation[index]['stopID']  # Find Statation Name again
=======
        return

    def getCurrentNearestStation(self):
        # TODO
        pass
>>>>>>> 56a3c28479e5cfa126af0cdf3c905cf778866315
