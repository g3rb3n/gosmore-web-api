import geopy
from geopy.location import Location

handler = lambda obj: (
    {
        'address':obj.address,
        'location':{
            'latitude':obj.latitude,
            'longitude':obj.longitude
        }
    }
    if isinstance(obj, Location)
    else None
)