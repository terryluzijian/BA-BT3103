import requests
import json


class Route(object):
    """docstring for Route"""
    # TODO
    travelSpeed = {}  # Including all possible Means
    travelFare = {}  # Functions of fare

    def __init__(self, RouteFrom, RouteTo, Means):  # EstimatedArrivalTime, EstimatedDistance, EstimatedFare):
        self.RouteFrom = RouteFrom
        self.RouteTo = RouteTo
        self.Means = Means
        # self.EstimatedArrivalTime = EstimatedArrivalTime
        # self.EstimatedDistance = EstimatedDistance
        # self.EstimatedFare = EstimatedFare

    def getFrom(self):
        return self.RouteFrom

    def getTo(self):
        return self.RouteTo

    def getMeans(self):
        return self.Means

    def getEstimatedArrivalTime(self):
        return self.EstimatedDistance(self) / Route.travelSpeed[self.getMeans(self)]

    def getEstimatedDistance(self):
        return json.loads((requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + str(self.RouteFrom) + '&destinations=' + str(self.RouteTo) + '&key=AIzaSyB7oKsCG5uN6nTGRj1KjvIr0ZJuC7rMAXo').content))['rows'][0]['elements']['distance']['value']

    def getEstimatedFare(self):
        return Route.travelFare[self.getMeans(self)](self.getEstimatedDistance(self))
