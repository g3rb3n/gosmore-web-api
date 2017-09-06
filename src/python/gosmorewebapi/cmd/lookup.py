import json
import argparse
from geopy.geocoders import Nominatim

import gosmorewebapi.gosmore as gosmore
from gosmorewebapi.util.geopy_json import handler

geolocator = Nominatim()
        
parser = argparse.ArgumentParser(description='lookup an address by query')
parser.add_argument('query')
args = parser.parse_args()

location = geolocator.geocode(args.query)

print(json.dumps(location, default=handler, indent=2))
