from datetime import date, time, datetime
from bson.json_util import ObjectId
from decimal import Decimal
import json
from bunnet import Document

# Custom json encoder
class MongoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date): return str(obj)
        if isinstance(obj, time): return str(obj)
        if isinstance(obj, datetime): return str(obj)
        if isinstance(obj, ObjectId): return str(obj)
        if isinstance(obj, Decimal): return float(obj)
        if isinstance(obj, Exception): return str(obj)
        if isinstance(obj, bytes):
            return int.from_bytes(obj, byteorder='big') if len(obj)==1 else obj.decode()
        if isinstance(obj, Document): return obj.dict()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
