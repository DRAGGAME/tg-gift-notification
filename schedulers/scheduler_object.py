import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
loop = asyncio.get_event_loop_policy().get_event_loop()
scheduler = AsyncIOScheduler(loop=loop)
