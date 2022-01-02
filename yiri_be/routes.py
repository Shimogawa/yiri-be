from typing import Dict, Type
from yiri_be.backend import YiriBEViewBase
from yiri_be.views.bot import GetBotStatusView
from yiri_be.views.handler import (
    DeleteHandlerView,
    GetHandlerView,
    NewHandlerView,
    UpdateHandlerView,
)
from yiri_be.views.messages import SendFriendMessageView


routes: Dict[str, Type[YiriBEViewBase]] = {
    "/bot/status": GetBotStatusView,
    "/bot/message/private/send": SendFriendMessageView,
    "/bot/handler/new": NewHandlerView,
    "/bot/handler/get": GetHandlerView,
    "/bot/handler/update": UpdateHandlerView,
    "/bot/handler/delete": DeleteHandlerView,
}
