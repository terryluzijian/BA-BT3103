campusStation = []


class publicTransport(object):
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
        return

    def getCurrentNearestStation(self):
        # TODO
        pass
