import gpxpy
import pygeohash as pgh
import time
from geoconv import GeoConv
from os.path import splitext


class Map:
    def __init__(self, points, ctx):
        """
        Instantiate an Map object with path corodinates added to the Map object
        :param points: a list of tuples contains latitude and longitude
        """
        self._points = points

        self.google_coordinates = ",\n".join(
            [f'{{lat: {lat}, lng: {lng}}}' for lat, lng, *rest in self._points]
        )

        self.baidu_coordinates = []

        geo = GeoConv(ctx["BAIDU_WEB_KEY"])
        """
        baidu_points = geo.gps_to_baidu(
            [(lng, lat) for lat, lng, *rest in self._points]
        )
        self.baidu_coordinates = ",\n".join(
            [f'{{lat: {lat}, lng: {lng}}}' for lng, lat in baidu_points]
        )
        """

        baidu_path = geo.gps_to_baidu_track(
            [(lng, lat, time.mktime(t.timetuple()))
             for lat, lng, e, t in self._points]
        )
        self.baidu_coordinates_path = ",\n".join(
            [f'{{lat: {lat}, lng: {lng}}}' for lng, lat in baidu_path]
        )


class GPX:
    def __init__(self, gpx_file):
        self.title = splitext(gpx_file)[0]
        self.trackpoints = []

        with open(gpx_file) as gf:
            gpx = gpxpy.parse(gf)

        # gpx.simplify(max_distance=10)

        last_hash = 0
        for track in gpx.tracks:
            for segment in track.segments:
                for i, p in enumerate(segment.points):
                    geo_hash = pgh.encode(p.latitude, p.longitude, precision=9)
                    if last_hash == geo_hash:
                        continue

                    self.trackpoints.append(
                        (p.latitude, p.longitude, p.elevation, p.time)
                    )
                    last_hash = geo_hash

        print(len(self.trackpoints))
