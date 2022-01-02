import sys
import os

sys.path.append(".")

import yiri_be.backend as be
from mirai import Mirai, WebSocketAdapter, MessageEvent


bot = Mirai(
    int(os.environ["QQ"]),
    WebSocketAdapter(os.environ.get("VERIFY_KEY"), "127.0.0.1", 4500),
)
# bot = Mirai(
#     qq=0,
#     adapter=WebSocketAdapter(
#         verify_key=None, host="127.0.0.1", port=4500, single_mode=True
#     ),
# )


async def handle_message_event(event: MessageEvent):
    print("MessageEvent")


bot.subscribe("MessageEvent", handle_message_event)


be.register_routes()
be.start_server(bot, "sqlite:///db/a.sqlite3")

bot.run()
