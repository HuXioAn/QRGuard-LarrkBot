from nonebot import on_regex
from nonebot.adapters.feishu import Bot, Event
from .qinqiong import *

Door = on_regex(pattern=r"^(.|\n)*$", priority=15, block=False)

@Door.handle()
async def door_handle(bot: Bot, event: Event):
    id = str(event.get_user_id())
    planar(id)