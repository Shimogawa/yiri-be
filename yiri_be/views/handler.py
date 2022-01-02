from typing import Any, Dict
from yiri_be.backend import YiriBEViewBase, not_found
from yiri_be.handlers import register_handler, unregister_handler, get_handler
from yiri_be.handlers.handler import update_handler

from marshmallow import fields


class NewHandlerView(YiriBEViewBase):
    request_schema = {
        "name": fields.String(required=True),
        "type": fields.String(required=True),
        "code": fields.String(required=True),
    }
    methods = ["POST"]

    def handle_req(self, req: Dict[str, Any]):
        register_handler(req["name"], req["type"], req["code"])


class DeleteHandlerView(YiriBEViewBase):
    request_schema = {
        "name": fields.String(required=True),
    }
    methods = ["POST"]

    def handle_req(self, req: Dict[str, Any]):
        unregister_handler(req["name"])


class UpdateHandlerView(YiriBEViewBase):
    request_schema = {
        "name": fields.String(required=True),
        "code": fields.String(),
    }
    methods = ["POST"]

    def handle_req(self, req: Dict[str, Any]) -> Any:
        update_handler(req["name"], req.get("code"))


class GetHandlerView(YiriBEViewBase):
    request_schema = {
        "name": fields.String(required=True),
    }
    response_schema = {
        "name": fields.String(),
        "code": fields.String(),
        "type": fields.String(),
    }
    methods = ["GET"]

    def handle_req(self, req: Dict[str, Any]):
        h = get_handler(req["name"])
        if not h:
            not_found()
        return {"name": h.name, "code": h.script, "type": h.type}
