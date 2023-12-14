import asyncio
import itertools


async def waiter(event):
    print('waiting for it ...')
    await event.wait()
    print('... got it!')

async def producer(queue: asyncio.Queue, queue2: asyncio.Queue):
    """producer emulator, creates ~ 10 tasks per second"""
    sleep_seconds = 1
    counter = itertools.count(1)
    run = 1
    i = 0
    while run == 1:
        await queue.put(next(counter))
        await queue2.put(next(counter))
        await asyncio.sleep(sleep_seconds)
        i += 1

        if i >= 20:
            run = 0
            print("Task Ended")
            # break


async def consumer(queue: asyncio.Queue, index, queue2: asyncio.Queue):
    """slow io-bound consumer emulator, process ~ 5 tasks per second"""
    sleep_seconds = 4
    while True:
        task = await queue.get()
        print(f"consumer={index}, task={task}, queue_size={queue.qsize()}")
        await asyncio.sleep(sleep_seconds)

        # await queue2.put(task)
        queue.task_done()


async def consumer2(queue: asyncio.Queue, index):
    """slow io-bound consumer emulator, process ~ 5 tasks per second"""

    sleep_seconds = 1
    while True:
        task = await queue.get()
        print(f"consumer2={index}, task2={task}, queue_size2={queue.qsize()}")
        # print(data_opcua)
        await asyncio.sleep(sleep_seconds)


async def main():
    # q = asyncio.Queue()
    # q2 = asyncio.Queue()
    # event = asyncio.Event()

    concurrency = 1  # consumers count
    # await asyncio.gather(producer(q), consumer2(q2, 1), consumer(q, 1, q2) , main_function(data_opcua))

if __name__ == "__main__":
    asyncio.run(main())