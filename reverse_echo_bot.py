# reverse_echo_bot.py
# pip install botbuilder-core aiohttp

import os
from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity, ActivityTypes

# Azure registration credentials (leave empty while you test with the Emulator)
APP_ID       = os.getenv("MicrosoftAppId", "")
APP_PASSWORD = os.getenv("MicrosoftAppPassword", "")

adapter = BotFrameworkAdapter(BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD))


async def on_message(turn: TurnContext):
    if turn.activity.type == ActivityTypes.message:
        await turn.send_activity((turn.activity.text or "")[::-1])   # 🔄 reverse & reply


# Very tiny error handler
adapter.on_turn_error = lambda ctx, err: ctx.send_activity("oops – " + str(err))

# Single POST endpoint Teams will call
async def messages(req: web.Request):
    body        = await req.json()
    activity    = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")
    resp        = await adapter.process_activity(activity, auth_header, on_message)
    return web.json_response(data=resp.body, status=resp.status) if resp else web.Response()

app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, port=3978)   # Teams Toolkit & Bot Emulator both look here by default



