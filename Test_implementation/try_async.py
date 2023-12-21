import asyncio

async def producer(queue, max_events):

        queue.put_nowait("Start")
        print(f"Produced: {"Start"}")

      # Signal the end of events

async def consumer(queue, consumer_name, t):
    while True:
        event = await queue.get()
        print(f"{consumer_name} Consumed: {event}")
        await asyncio.sleep(3)
        t += 1
        if t == 4:
            queue.task_done()
        elif t < 4:
            queue.put_nowait(event)


async def main():
    queue1 = asyncio.Queue()
    queue2 = asyncio.Queue()
    queue3 = asyncio.Queue()

    max_events = 5

    producers = [
        producer(queue1, max_events),
    ]

    consumers = [
        consumer(queue1, "Consumer 1", t=t),

    ]

    await asyncio.gather(*producers, *consumers)

if __name__ == "__main__":
    t = 0
    asyncio.run(main())