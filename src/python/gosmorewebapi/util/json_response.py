import json
from flask import Response
from functools import wraps
import datetime

date_handler = lambda obj: (
    obj.isoformat() + 'Z'
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else None
)

def json_response(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        return Response(json.dumps(f(*args, **kwargs), default=date_handler), mimetype='application/json')
    return wrapped_function
