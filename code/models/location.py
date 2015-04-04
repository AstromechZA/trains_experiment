from validoot import validates, longitude as vlongitude, latitude as vlatitude, inst

import math


class Location(object):
    """
    A location on the earth specified by a latitude and longitude.
    """

    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon

    def __repr__(self):
        return "Location({},{})".format(self.latitude, self.longitude)

    def __str__(self):
        return "Location(lat={},lon={})".format(self.latitude, self.longitude)

    def __eq__(self, other):
        return self.latitude == other.latitude and self.longitude == other.longitude

    @property
    def latitude(self):
        return self.latitude

    @validates(vlatitude)
    @latitude.setter
    def latitude(self, value):
        self.latitude = value

    @property
    def longitude(self):
        return self.longitude

    @validates(vlongitude)
    @longitude.setter
    def longitude(self, value):
        self.longitude = value

    def distance(self, other):
        """
        Haversine great circle distance
        :return: the distance in kilometers
        """

        d_lat = math.radians(other.latitude - self.latitude)
        d_lon = math.radians(other.longitude - self.longitude)
        lat1 = math.radians(self.latitude)
        lat2 = math.radians(other.latitude)
        a = (math.sin(d_lat/2) ** 2) + (math.sin(d_lon/2) ** 2) * math.cos(lat1) * math.cos(lat2)
        return 6372.8 * 2 * math.asin(math.sqrt(a))

    def distance_fast(self, other):
        """
        Pythagoras Equirectanglar approximation
        :return: the distance in kilometers
        """
        d_lat = math.radians(other.latitude - self.latitude)
        d_lon = math.radians(other.longitude - self.longitude)
        s_lon = math.radians(other.longitude + self.longitude)
        x = d_lat * math.cos(s_lon / 2.0)
        return math.sqrt(x * x + d_lon * d_lon) * 6372.8

    def bearing(self, other):
        """
        Calculate the initial bearing (forward azimuth) toward the other point
        :return: the bearing in degrees
        """
        d_lon = math.radians(other.longitude - self.longitude)
        lat1 = math.radians(self.latitude)
        lat2 = math.radians(other.latitude)
        y = math.sin(d_lon) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
        return math.degrees(math.atan2(y, x))


# Can only do these internal references afterwards. Messy, but no alternative.
Location.distance = validates(inst(Location))(Location.distance)
Location.distance_fast = validates(inst(Location))(Location.distance_fast)
Location.bearing = validates(inst(Location))(Location.bearing)
