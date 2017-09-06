# Gosmore web api
A python wrapper around the Gosmore routing engine executable based on geopy and flask.

# Testing
make test

# Command line usage
cd src/python
python3 -m gosmorewebapi.route --from "My current address" --to "My destination address" --vehicle bicycle
cd ../..


# Example
```
import gosmorewebapi.gosmore as gosmore
a = {
    "latitude":53.04821,
    "longitude":5.65922
}
b = {
    "latitude":53.02616,
    "longitude":5.66875
}

errors = []
route = gosmore.route(a, b, errors, 'foot', True)
distance = gosmore.distance(route)
formatted = gosmore.format_geo_json(route, distance)
print(formatted)
```