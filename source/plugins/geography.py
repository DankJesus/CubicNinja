from geopy.geocoders import Nominatim
from geopy.distance import vincenty
geolocator = Nominatim()

def getCoordinates(location):
    n = geolocator.geocode(location)
    if n == None: return
    return (n.latitude, n.longitude)

def getDistance(location1, location2):
    return vincenty(location1, location2).miles
