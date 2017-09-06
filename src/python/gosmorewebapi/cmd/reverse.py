import json
import argparse
import geopy
from geopy.geocoders import Nominatim
from geopy.location import Location

import gosmorewebapi.gosmore as gosmore
from gosmorewebapi.util.geopy_json import handler

geolocator = Nominatim()
        
parser = argparse.ArgumentParser(description='reverse lookup')
parser.add_argument('latitude', type=float)
parser.add_argument('longitude', type=float)
args = parser.parse_args()

location = geolocator.reverse((args.latitude, args.longitude))

print(json.dumps(location, default=handler, indent=2))
