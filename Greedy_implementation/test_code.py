
import asyncio

async def myCoroutine():
    while True:
        await asyncio.sleep(1)
        print("My  coroutine")


loop = asyncio.get_event_loop()

try :
    asyncio.ensure_suture(myCoroutine())

