from typing import Any, Dict

from marshmallow import fields
from marshmallow.schema import Schema


class Nested(fields.Nested):
    def __init__(self, dict: Dict[str, Any], *args, **kwargs):
        fields.Nested.__init__(self, Schema.from_dict(dict), *args, **kwargs)
