from typing import Dict
from marshmallow import fields

from mirai.models.message import MessageChain
import yiri_be.backend as be


class SendFriendMessageView(be.YiriBEViewBase):
    request_schema = {
        "target": fields.Integer(required=True),
        "message_chain": fields.List(fields.Dict(keys=fields.Str()), required=True),
        "quote": fields.Boolean(),
    }
    response_schema = {
        "message_id": fields.Integer(),
    }
    methods = ["POST"]

    async def handle_req(self, req: Dict[str, str]):
        msg_resp = await be._bot.send_friend_message(
            req["target"], MessageChain(req["message_chain"]), req.get("quote")
        )
        if msg_resp.code != 0:
            return be.YiriBEError(msg_resp.code, msg_resp.msg)
        return {"message_id": msg_resp.message_id}
