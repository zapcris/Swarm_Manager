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


# async def execution_time(flag, id):
#
#     while True:
#         # print(f'waiting for robot {id} for  execution')
#         await flag.wait()
#         print(f'Robot {id} execution timer has started')
#         #await asyncio.sleep(3)
#         start_time = datetime.now()
#         Events["rob_execution"][id - 1] = True
#         while Events["rob_execution"][id - 1] == True:
#             if data_opcua["rob_busy"][id - 1] == True:
#                 # exec_time = (datetime.now() - start_time).total_seconds()
#                 # print(f"Robot {id} is running")
#                 pass
#             elif data_opcua["rob_busy"][id - 1] == False:
#                 Events["rob_execution"][id - 1] = False
#         exec_time = (datetime.now() - start_time).total_seconds()
#
#         flag.clear()
#
#         return print(f"Robot {id} took {exec_time:,.2f} seconds to run")
#
#
# async def process_execution(event, wk, product_pv):
#     process_time = order["Process_times"][product_pv][wk-1]
#     await event.wait()
#     print(f"Process task executing at workstation {wk}")
#     await asyncio.sleep(process_time)
#     print("Process task completed on workstation ",wk )
#     #prod_release()
#     event.clear()