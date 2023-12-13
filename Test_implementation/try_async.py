import asyncio

async def producer(queue, max_events):
    for i in range(max_events):
        await asyncio.sleep(1)  # Simulate an event every second
        event = f"Event {i + 1}"
        await queue.put(event)
        print(f"Produced: {event}")

    await queue.put(None)  # Signal the end of events

async def consumer(queue, consumer_name):
    while True:
        event = await queue.get()
        if event is None:
            # End the consumer loop when the sentinel value is received
            break

        print(f"{consumer_name} Consumed: {event}")
        await asyncio.sleep(2)  # Simulate some processing time

async def main():
    queue1 = asyncio.Queue()
    queue2 = asyncio.Queue()
    queue3 = asyncio.Queue()

    max_events = 5

    producers = [
        producer(queue1, max_events),
    ]

    consumers = [
        consumer(queue1, "Consumer 1"),
        consumer(queue2, "Consumer 2"),
        consumer(queue3, "Consumer 3"),
    ]

    await asyncio.gather(*producers, *consumers)

if __name__ == "__main__":
    asyncio.run(main())