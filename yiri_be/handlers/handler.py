from typing import Callable, Dict, List, Optional, Union
import inspect
import traceback

import yiri_be.backend as be
from yiri_be.database import dbcommit
import yiri_be.models as m

import mirai.models.events

__all__ = [
    "SUPPORTED_EVENT_TYPES",
    "YiriBEHandler",
    "handler_script_to_func",
    "register_handler",
    "get_handler",
    "unregister_handler",
    "init_handlers",
]


SUPPORTED_EVENT_TYPES = {
    name
    for name, obj in inspect.getmembers(mirai.models.events)
    if inspect.isclass(obj) and issubclass(obj, mirai.models.events.Event)
}


class YiriBEHandler:
    def __init__(
        self, name: str, event_type: str, func: Callable, priority: int = 0
    ) -> None:
        self._name = name
        self._event_type = event_type
        self._func = func
        self._priority = priority

    @property
    def name(self):
        return self._name

    @property
    def event_type(self):
        return self._event_type

    @property
    def func(self):
        return self._func

    @property
    def priority(self):
        return self._priority


handlers: Dict[str, YiriBEHandler] = {}


def handler_script_to_func(script: str) -> Callable:
    if len(script) == 0 or script.isspace():
        raise be.YiriBEError(400, "No code present")
    script = "".join(map(lambda x: "    " + x, script.split("\n")))
    script = f"async def _f_(event):\n{script}"

    # async def _f_(event):
    loc: dict = {}

    try:
        exec(script, {"bot": be._bot}, loc)
    except SyntaxError:
        exc_str = traceback.format_exc(1).split("\n")
        s = exc_str[0] + "\n" + "\n".join(exc_str[3:])
        raise be.YiriBEError(499, s)

    return loc["_f_"]


def _register_to_mem(name: str, event_type: str, func: Callable, priority: int = 0):
    if name in handlers:
        raise be.YiriBEError(400, "Name of handler already used")
    if event_type not in SUPPORTED_EVENT_TYPES:
        raise be.YiriBEError(400, f"Event type not supported: {event_type}")
    if not callable(func):
        raise be.YiriBEError(500, f"func not callable")
    be._bot.subscribe(event_type, func, priority)
    handlers[name] = YiriBEHandler(name, event_type, func, priority)


def _del_from_mem(name: str):
    if name not in handlers:
        return
    handler = handlers[name]
    be._bot.unsubscribe(handler.event_type, handler.func)
    handlers.pop(name)


@dbcommit
def register_handler(
    name: str,
    event_type: str,
    func: Union[Callable, str],
    priority: int = 0,
):
    hl_model = None
    if isinstance(func, str):
        hl_model = m.Handler(name=name, type=event_type, script=func, priority=priority)
        func = handler_script_to_func(func)
    _register_to_mem(name, event_type, func, priority)
    if hl_model:
        hl_model.insert()


@dbcommit
def unregister_handler(name: str):
    _del_from_mem(name)
    # if m.Handler.query.filter(m.Handler.name == name).count() == 0:
    #     return
    m.Handler.query.filter(m.Handler.name == name).delete()


def get_handler(name: str) -> Optional[m.Handler]:
    handler = m.Handler.query.filter(m.Handler.name == name).first()
    return handler


def update_handler(name: str, code: Optional[str] = None):
    handler = get_handler(name)
    if not handler:
        be.not_found()
    modified = False
    if code is not None and code != handler.script:
        modified = True
        handler.script = code
    if modified:
        _del_from_mem(name)
        _register_to_mem(
            name, handler.type, handler_script_to_func(handler.script), handler.priority
        )
        handler.save()


def init_handlers():
    all_handlers: List[m.Handler] = m.Handler.query.all()
    for handler in all_handlers:
        _register_to_mem(
            handler.name,
            handler.type,
            handler_script_to_func(handler.script),
            handler.priority,
        )
