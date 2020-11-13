"""
Base class for implementing PynamoDB models.
Provides a to_dict() method for deserializing
"""
import os
from datetime import datetime

from pynamodb.attributes import MapAttribute
from pynamodb.models import Model

DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")


class BaseModel(Model):
    class Meta:
        table_name = DYNAMODB_TABLE_NAME

    def to_dict(self):
        ret_dict = {}
        for name, attr in self.attribute_values.items():
            ret_dict[name] = self._attr2obj(attr)

        return ret_dict

    def _attr2obj(self, attr):
        # compare with list class. It is not ListAttribute.
        if isinstance(attr, list):
            _list = []
            for item in attr:
                _list.append(self._attr2obj(item))
            return _list
        elif isinstance(attr, MapAttribute):
            _dict = {}
            for k, v in attr.attribute_values.items():
                _dict[k] = self._attr2obj(v)
            return _dict
        elif isinstance(attr, datetime):
            return attr.isoformat()
        else:
            return attr
