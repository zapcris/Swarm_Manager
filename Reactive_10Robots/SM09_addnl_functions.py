import asyncio
from asyncio import AbstractEventLoop



class Event_ts(asyncio.Event):
    def __init__(self, _loop: AbstractEventLoop):
        super().__init__()
        self._loop = _loop
        # if self._loop is None:
        #     self._loop = asyncio.get_event_loop()

    def set(self):
        self._loop.call_soon_threadsafe(super().set)

    def clear(self):
        self._loop.call_soon_threadsafe(super().clear)


def event_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()

event =asyncio.Event()
def done():
    event.set()


async def firstWorker():
    while True:
        await event.wait()
        print("First Worker Executed")
        event.clear()

async def secondWorker():
    while True:
        await asyncio.sleep(1)
        print("Second Worker Executed")


