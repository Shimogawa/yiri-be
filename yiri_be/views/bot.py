from typing import Dict
import yiri_be.backend as be
from marshmallow import fields


class GetBotStatusView(be.YiriBEViewBase):
    request_schema: dict = {}
    response_schema = {"version": fields.String()}
    methods = ["GET"]

    async def handle_req(self, req: Dict[str, str]):
        resp = await be._bot.about()
        return resp.data
