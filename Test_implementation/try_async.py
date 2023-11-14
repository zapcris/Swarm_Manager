import asyncio

async def waiter():
    print('waiting for it ...')

    await asyncio.sleep(5)

    print('... got it!')

async def main():
    # Create an Event object.
    event = asyncio.Event()

    # Spawn a Task to wait until 'event' is set.
    waiter_task = asyncio.create_task(waiter())
    print("event_created")

    # Sleep for 1 second and se

    # Wait until the waiter task is finished.
    await waiter_task


async def main2():
    # Create an Event object.

    print("main task running")

    await asyncio.sleep(1)

    print("main task running2")
    await asyncio.sleep(1)

    print("main task running3")

    await asyncio.sleep(1)

    print("main task running4")





asyncio.run(main())
asyncio.run(main2())