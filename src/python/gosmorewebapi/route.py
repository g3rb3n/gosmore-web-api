import json
import argparse
from geopy.geocoders import Nominatim

import gosmorewebapi.gosmore as gosmore

geolocator = Nominatim()
        
parser = argparse.ArgumentParser(description='gosmore py wrapper.')
parser.add_argument('--flat', dest='from_latitude', type=float, help='latitude')
parser.add_argument('--flon', dest='from_longitude', type=float, help='longitude')
parser.add_argument('--tlat', dest='to_latitude', type=float, help='latitude')
parser.add_argument('--tlon', dest='to_longitude', type=float, help='longitude')
parser.add_argument('--from', dest='start')
parser.add_argument('--to', dest='end')
parser.add_argument('--vehicle', dest='vehicle', default='motorcar')
parser.add_argument('--fastest', dest='fastest', type=bool, default=True)

args = parser.parse_args()

if (args.start):
    location = geolocator.geocode(args.start)
    args.from_latitude = location.latitude
    args.from_longitude = location.longitude

if (args.end):
    location = geolocator.geocode(args.end)
    args.to_latitude = location.latitude
    args.to_longitude = location.longitude

start = {
    "latitude":args.from_latitude,
    "longitude":args.from_longitude
}

end = {
    "latitude":args.to_latitude,
    "longitude":args.to_longitude
}

try:
	errors = []
	route = gosmore.route(start, end, fastest=args.fastest, vehicle=args.vehicle, error_collector=errors)
	distance = gosmore.distance(route)
	output = gosmore.format_kml(route, distance)

	for waypoint in route:
	    print(json.dumps(waypoint))

	for err in errors:
	    print(err)
except e:
	print('Error:' + e)