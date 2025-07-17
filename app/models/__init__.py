import re
from pydantic import PrivateAttr
from bunnet import Document
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from pydantic import ValidationError
from app.exceptions import InvalidDataError
from bunnet.odm.utils.dump import get_dict

# Make sure to add model in document_models in db.py
class BaseDocument(Document):
    created_at: datetime | None = None
    updated_at: datetime | None = None
    _changes: dict = PrivateAttr(default={})

    @property
    def _id(self):
        return str(self.id)

    def insert(self, *args, **kwargs):
        try:

            self.created_at = datetime.now()
            self.updated_at = self.created_at
            return Document.insert(self, *args, **kwargs)

        except ValidationError as e:
            error_message = ", ".join([f"{', '.join(err['loc'])} {err['msg']}" for err in e.errors()])
            raise InvalidDataError(error_message)

        except DuplicateKeyError as e:
            key_search = re.search("'keyValue': {'([a-zA-Z_]*)': ([a-zA-z_]*)", str(e), re.IGNORECASE)
            error_message = f"{key_search.group(1)}: {key_search.group(2)} already in use"
            raise InvalidDataError(error_message)

    def insert_one(obj, *args, **kwargs):
        return obj.insert(*args, **kwargs)

    def insert_many(objs, *args, **kwargs):
        return [obj.insert(*args, **kwargs) for obj in objs]

    def _update(self, request, *args, **kwargs):
        if not self.created_at:
            request['created_at'] = datetime.now()
        request['updated_at'] = datetime.now()

        if self.use_state_management():
            for key, value in request.items():
                setattr(self, key, value)

            self._set_changes()
            self.save_changes(*args, **kwargs)
        else:
            self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if '$set' not in request:
            request = {'$set': request}
        Document.update(self, request, *args, **kwargs)

    def save_changes(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self._set_changes()
        Document.save_changes(self, *args, **kwargs)

    def _set_changes(self):
        self._changes = self._get_changes()

    def _get_changes(self):
        if not self._saved_state: return {}

        changes = {}
        old_dict, new_dict = self._saved_state, get_dict(self, to_db=True)
        for field_name, field_value in new_dict.items():
            if field_value != old_dict.get(field_name):
                changes[field_name] = [old_dict.get(field_name), field_value]
        return changes
