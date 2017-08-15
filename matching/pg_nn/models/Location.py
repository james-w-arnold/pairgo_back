import googlemaps
import json
import pprint
import logging
class Location:

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def getLatLon(self):
        return "{},{}".format(self.lat, self.lon)

    def __str__(self):
        return "{},{}".format(self.lat, self.lon)


class LocationComparator:
    """
    This class uses the google maps api to compare the different locations offered by the user against the location
    specified for the posting by the employer
    """
    def __init__(self, posting_location, candidate_locations):
        self.api_key = "AIzaSyDbkAJndXb-HX6cj4LYYaB8Nm98DmI3D7Y"
        self.posting_location = posting_location
        self.candidate_locations = []
        self.max_distance = 100000
        self.min_distance = 0

        for item in candidate_locations:
            self.candidate_locations.append(item)

    def testPrint(self):
        print("{} | {}".format(self.posting_location, self.candidate_locations))

    def changePostingLocation(self, location):
        self.posting_location = location

    def addCandidateLocation(self, location):

        if location not in self.candidate_locations:
            self.candidate_locations.append(location)

    def getShortestDistance(self):
        #construct maps request

        try:
            gmaps = googlemaps.Client(key=self.api_key)
            origin = self.posting_location.getLatLon()
            destinations = []

            for loc in self.candidate_locations:
                destinations.append(loc.getLatLon())


            distmatx = gmaps.distance_matrix(
                origin,
                destinations
            )
            #from returned values, return the smallest distance
            #pprint.pprint(distmatx)
            rows = distmatx['rows']

            shortest_row = rows[0]['elements'][0]['distance']['value']

            if len(rows[0]['elements']) > 1:
                for item in rows:
                    for value in item.values():
                        for val in value:
                            if val['distance']['value'] < shortest_row:
                                shortest_row = val['distance']['value']
            if shortest_row > self.max_distance:
                return 1
            elif type(shortest_row) is None:
                return 1
            else:
                if shortest_row is not None:
                    return shortest_row/self.max_distance
                else:
                    return 1

        except AssertionError as e:
            raise AssertionError('Locations need to be location object')
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(e)





if __name__ == '__main__':
    norwich = Location(52.6388845,1.2273144)
    chelmsford = Location(51.7258701,0.4090747)
    norwich2 = Location(52.6217286,1.2793956)
    romford = Location(51.5917918,0.1321445)

    comparator = LocationComparator(chelmsford, [norwich, norwich2, romford])
    comparator.testPrint()
    result = comparator.getShortestDistance()
    print(result)
