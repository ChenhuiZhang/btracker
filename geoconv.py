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


if __name__ == "__main__":
    key = os.environ.get("BAIDU_WEB_KEY")
    geo = GeoConv(key)
    gps = [(114.21892734521, 29.575429778924)]
    baidu = geo.gps_to_baidu(gps)
    print(f'GPS:   {gps[0]}\n'
          f'Baidu: {baidu[0]}')
