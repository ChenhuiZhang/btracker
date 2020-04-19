import requests
import json
import os
import logging


class GeoConv:
    def __init__(self, key):
        self.key = key

    def gps_to_baidu(self, points):
        coords = ""
        for p in points:
            coords += f"{p[0]},{p[1]};"

        logging.debug(coords[:-1])

        URL = (
            f'http://api.map.baidu.com/geoconv/v1/?'
            f'coords={coords[:-1]}&from=1&to=5&ak={self.key}'
        )
        proxy = {}
        r = requests.get(URL, proxies=proxy)
        logging.debug(r.text)
        j = json.loads(r.text)

        if j["status"] != 0:
            logging.error(f'Status: {j["status"]} for {j["message"]}')
            return [()]

        result = []
        for e in j["result"]:
            result.append((e["x"], e["y"]))

        return result

    def gps_to_baidu_track(self, points):
        coords = []
        for p in points:
            coords.append({
                'coord_type_input': "wgs84",
                'longitude': p[0],
                'latitude': p[1],
                'loc_time': p[2]
            })

        URL = (
            f'http://api.map.baidu.com/rectify/v1/track?'
        )
        proxy = {}
        data = {
            'ak': self.key,
            'point_list': json.dumps(coords),
            'rectify_option': "need_mapmatch:1|" + \
                              "transport_mode:auto|" + \
                              "denoise_grade:0|" + \
                              "vacuate_grade:1",
            'coord_type_output': "bd09ll"
        }
        r = requests.post(URL, proxies=proxy, data=data)

        j = json.loads(r.text)

        result = []
        for e in j["points"]:
            result.append((e["longitude"], e["latitude"]))

        return result


if __name__ == "__main__":
    key = os.environ.get("BAIDU_WEB_KEY")
    geo = GeoConv(key)
    gps = [(120.593674, 31.30108, 1584212796),
           (120.59406, 31.305869, 1584213104)]
    baidu = geo.gps_to_baidu(gps)
    print(f'GPS:   {gps[0]}\n'
          f'Baidu: {baidu[0]}')
