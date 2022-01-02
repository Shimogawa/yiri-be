from abc import ABC, abstractmethod
from typing import (
    Any,
    Dict,
    Iterable,
    NoReturn,
    Optional,
    Type,
    Union,
    no_type_check,
)
from flask import Flask, request
from marshmallow import Schema
from marshmallow.exceptions import ValidationError
from mirai import Mirai
import threading
import inspect
import atexit

from yiri_be.database import init_db
from yiri_be.handlers import init_handlers

# import traceback

_bot: Mirai = None

__all__ = [
    "Response",
    "YiriBEError",
    "YiriBEViewBase",
    "bad_request",
    "start_server",
    "stop_server",
    "register_routes",
]

_app = Flask(__name__)
_started = False
_app_thread = None


class Response:
    def __init__(self, code: int, message: Optional[str], data: Any) -> None:
        self._code = code
        self._message = message
        self._data = data

    @property
    def code(self) -> int:
        return self._code

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def data(self) -> Any:
        return self._data


class YiriBEError(RuntimeError, Response):
    def __init__(
        self, code: int, message: Optional[str] = None, data: Optional[str] = None
    ) -> None:
        Response.__init__(self, code, message, data)
        RuntimeError.__init__(self, message)


class YiriBEViewBase(ABC):
    request_schema: Dict[str, Any]
    response_schema: Dict[str, Any]
    methods: Union[Iterable[str], str]

    def __init__(self):
        self._req_sch: Schema = (
            Schema.from_dict(self.request_schema)()
            if getattr(self, "request_schema", None) is not None
            else None
        )
        self._resp_sch: Schema = (
            Schema.from_dict(self.response_schema)()
            if getattr(self, "response_schema", None) is not None
            else None
        )

    def parse_request(self, req: Dict[str, Any]) -> Dict[str, Any]:
        if not self._req_sch:
            return req
        return self._req_sch.load(req)

    @abstractmethod
    def handle_req(self, req: Dict[str, Any]) -> Any:
        pass

    def parse_response(self, resp: Any) -> Any:
        if not isinstance(resp, dict) or not self._resp_sch:
            return resp
        return self._resp_sch.dump(resp)


def bad_request(msg: str) -> NoReturn:
    raise YiriBEError(400, msg)


def not_found(msg: Optional[str] = None) -> NoReturn:
    raise YiriBEError(404, msg if msg else "not found")


def _generator_func(route: str, view: YiriBEViewBase, methods: Iterable[str]):
    @_app.route(route, endpoint=route, methods=methods)
    async def _f_():
        if request.method != "GET" and not request.is_json:
            raise RuntimeError("Not json post request")
        if request.method == "GET":
            req = request.args.to_dict()
        else:
            req = request.json
        try:
            req = view.parse_request(req)
        except ValidationError as e:
            return {"code": 400, "message": str(e)}
        code = 0
        message = ""
        ret = None
        try:
            if inspect.iscoroutinefunction(view.handle_req):
                ret = await view.handle_req(req)
            else:
                ret = view.handle_req(req)
        except YiriBEError as e:
            code = e.code
            message = e.message if e.message else ""
        except Exception as e:
            code = 500
            # message = traceback.format_exc(1)
            message = str(e)
            raise e
        if isinstance(ret, Response):
            code = ret.code
            message = ret.message
            data = ret.data
        elif isinstance(ret, dict):
            try:
                data = view.parse_response(ret)
            except ValidationError as e:
                code = 500
        else:
            data = ret

        return {"code": code, "message": message, "data": data}


@no_type_check
def _register_route(route: str, view: YiriBEViewBase):
    methods = view.methods
    if not isinstance(methods, list):
        methods = [methods]
    # _app.add_url_rule(route, view_func=view_func, methods=methods)
    _generator_func(route, view, methods)


def register_routes(
    routes: Optional[Dict[str, Type[YiriBEViewBase]]] = None,
    strict_trailing_slash: bool = True,
):
    from .routes import routes as default_routes

    rts = routes if routes else default_routes
    for route, view in rts.items():
        _register_route(route, view())
        if not strict_trailing_slash:
            another_rt = route
            if route.endswith("/"):
                another_rt = route[:-1]
            else:
                another_rt = route + "/"
            if another_rt not in rts:
                _register_route(another_rt, view())


def _init(db_conn: str):
    init_db(db_conn)
    init_handlers()


def start_server(bot: Mirai, db_conn: str, **kwargs):
    global _app_thread, _bot, _started
    _bot = bot
    kwargs.setdefault("debug", False)
    _init(db_conn)
    _app_thread = threading.Thread(target=lambda: _app.run(**kwargs), daemon=True)
    _app_thread.start()
    _started = True
    # atexit.register(stop_server)


def stop_server():
    global _started, _app_thread
    if not _started or not _app_thread:
        return
    shutdown = request.environ.get("werkzeug.server.shutdown")
    if not shutdown:
        raise RuntimeError("Not werkzeug server")
    shutdown()
    _app_thread.join()
    _app_thread = None
    _started = False
