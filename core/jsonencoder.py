import json
from sqlalchemy.ext.declarative import DeclarativeMeta
import decimal
import datetime


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, int):
            return int(obj)
        elif isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    # this will fail on non-encodable values, like other classes
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = data.__str__()
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
