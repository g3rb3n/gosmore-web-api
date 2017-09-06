import gosmorewebapi.gosmore as gosmore

a = {
    "latitude":53.04821,
    "longitude":5.65922
}
b = {
    "latitude":53.02616,
    "longitude":5.66875
}

def route(a,b,vehicle):
    errors = []
    fastest = True
    route = gosmore.route(a, b, errors, vehicle, fastest)
    assert not len(errors), "Gosmore gave errors %s" % errors
    assert len(route) > 1, "Gosmore gave no route %s" % len(route)
    distance = gosmore.distance(route)
    assert distance > 1000, "The distance is too small %s" % distance
    formatted = gosmore.format_kml(route, distance)
    assert len(formatted) > 1024, "The kml output is too small %s" % len(formatted)
    formatted = gosmore.format_geo_json(route, distance)
    assert len(formatted) > 1024, "The geo json output is too small %s" % len(formatted)

def test_vehicles():
    vehicles = ['motorcar', 'bicycle', 'foot']
    for vehicle in vehicles:
        route(a,b,vehicle)

