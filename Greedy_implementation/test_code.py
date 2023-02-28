
import asyncio





async def say_hello():
    print('Hello')
    # asynchronous sleep of 1 second
    await asyncio.sleep(40)
    print('World')

# we initialise our event loop
loop = asyncio.get_event_loop()
# we run our coroutine in the event loop until it is completed
loop.run_until_complete(say_hello())
# close the event loop
loop.close()


