import logging
import subprocess
import os
import json

from geopy.distance import VincentyDistance
from geopy.point import Point

import gosmorewebapi.config as config

logger = logging.getLogger(__name__)

def check_bounds(p):
    return check_longitude(p['longitude']) and check_latitude(p['latitude'])

def check_longitude(v):
    return -180 <= v and v <= 180

def check_latitude(v):
    return -90 <= v and v <= 90

def point_in_pak(a, pak):
    if a['longitude'] < pak['west'] or \
        a['longitude'] > pak['east'] or \
        a['latitude'] < pak['south'] or \
        a['latitude'] > pak['north']:
        return False
    return True

def select_pak(a,b):
    for pak in config.paks:
        if point_in_pak(a, pak) and point_in_pak(b, pak):
            return pak['pak']
    logger.error('No pak found for %s %s' % (a,b))
    return None

def select_style(vehicle):
    if vehicle in config.styles:
        return config.styles[vehicle]
    return config.default_style

def create_query(a, b, vehicle, fastest):
    values = []
    keys = ['flat','flon','tlat','tlon','fast','v']
    values.append(a["latitude"])
    values.append(a["longitude"])
    values.append(b["latitude"])
    values.append(b["longitude"])
    values.append(fastest)
    values.append(vehicle)
    return '&'.join(['='.join([k, str(v)]) for k,v in zip(keys, values)])

def parse_output(output, error_collector):
    lines = output.split('\n\r')
    path = [line.split(',') for line in lines[1:] if len(line)]
    error_collector.extend([' '.join(el) for el in path if len(el) and len(el) != 6])
    path = [el for el in path if len(el) == 6]
    keys = ['latitude', 'longitude', 'type', 'style', 'number', 'name']
    path = [dict(zip(keys, el)) for el in path]
    for el in path:
        for k in el: 
            if k in list(['latitude', 'longitude']):
                el[k] = float(el[k])
            if k in list(['number']):
                el[k] = int(el[k])
    return path

def route_formatted(a, b, vehicle='motorcar', fastest=1, format='geojson'):
    path = route(a, b, [], vehicle, fastest)
    dist = distance(path)
    if format == 'geojson':
        return format_geo_json(path, dist)
    elif format == 'kml':
        return format_kml(path, dist)
    raise "Unknown format %s" % format

def route(a, b, error_collector=[], vehicle='motorcar', fastest=1):
    if not check_bounds(a):
        raise Exception('Start point coordinates are out of bounds')
    if not check_bounds(b):
        raise Exception('End point coordinates are out of bounds')
    if not vehicle in config.vehicles:
        raise Exception('Vehicle %s not allowed' % vehicle)

    pak = select_pak(a,b)
    if not pak:
        raise Exception('No pak file found for coordinates')
    style = select_style(vehicle)
    if not style:
        raise Exception('No style xml file found for vehicle %s' % vehicle)
        
    query = create_query(a,b, vehicle, fastest)
    env = os.environ.copy()
    env["QUERY_STRING"] = query
    os.chdir(config.working_dir)
    command = ["nice", "./gosmore", pak, style]
    result = subprocess.run(command, stdout=subprocess.PIPE, env=env)
    path = result.stdout.decode('utf-8')
    return parse_output(path, error_collector)

def distance(route):
    dist = 0
    for a,b in zip(route[:-2], route[1:]):
        dist += point_distance(a,b)
    return dist

def geoobj_to_geodict(p):
    return {'latitude':p.latitude, 'longitude':p.longitude}

def geodict_to_geoobj(p):
    return Point(latitude=p['latitude'], longitude=p['longitude'])

def point_distance(lla, llb):
    a = geodict_to_geoobj(lla)
    b = geodict_to_geoobj(llb)
    return VincentyDistance(a,b).meters

def format_kml(route, distance):
    kml = '<?kml version="1.0" encoding="UTF-8"?>\n'
    kml += '<kml xmlns="http://earth.google.com/kml/2.0">\n'
    kml += '  <Document>\n'
    kml += '    <name>KML</name>\n'
    kml += '    <open>1</open>\n'
    kml += '    <distance>' + str(distance) + '</distance>\n'
    kml += '    <description>KML export</description>\n'
    kml += '    <Folder>\n'
    kml += '      <name>Paths</name>\n'
    kml += '      <visibility>0</visibility>\n'
    kml += '      <description>Paths</description>\n'
    kml += '      <Placemark>\n'
    kml += '        <name>Tessellated</name>\n'
    kml += '        <visibility>0</visibility>\n'
    kml += '        <description><![CDATA[If the <tessellate> tag has a value of 1, the line will contour to the underlying terrain]]></description>\n'
    kml += '        <LineString>\n'
    kml += '          <tessellate>1</tessellate>\n'
    kml += '          <coordinates>\n'
    for el in route:
        kml += str(el["longitude"]) + "," + str(el["latitude"]) + "\n"
    kml += '          </coordinates>\n'
    kml += '        </LineString>\n'
    kml += '      </Placemark>\n'
    kml += '    </Folder>\n'
    kml += '  </Document>\n'
    kml += '</kml>\n'
    return kml


def format_geo_json(route, distance):
    geo = {
        'type': 'LineString',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'
            }
        },
        'coordinates':[],
        'properties': {
            'distance': 0,
            'description': 'GeoJSON route result created by gosmore'
        }
    }
    for el in route:
        geo['coordinates'].append([el['longitude'],el['latitude']])
    geo['properties']['distance'] = distance
    return json.dumps(geo, indent=2)
