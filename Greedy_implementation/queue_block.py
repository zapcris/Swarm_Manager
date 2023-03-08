import asyncio
import time
import threading

def do_it(started):
    '''Process tasks in the queue until the sentinel value is received'''
    _sentinel = 'STOP'

    def clock():
        return time.strftime("%X")

    async def process(name, total_time):
        status = f'{clock()} {name}_{total_time}:'
        print(status, 'START')
        current_time = time.time()
        end_time = current_time + total_time
        while current_time < end_time:
            print(status, 'processing...')
            await asyncio.sleep(1)
            current_time = time.time()
        print(status, 'DONE.')

    async def main():
        started.loop = asyncio.get_running_loop()
        started.queue = task_queue = asyncio.Queue()
        started.set()
        while True:
            item = await task_queue.get()
            if item == _sentinel:
                task_queue.task_done()
                break
            task = asyncio.create_task(process(*item))
            task.add_done_callback(lambda _: task_queue.task_done())
        await task_queue.join()

    print('event loop start')
    asyncio.run(main())
    print('event loop end')

if __name__ == '__main__':
    started = threading.Event()
    th = threading.Thread(target=do_it, args=(started,))
    th.start()
    started.wait()
    tasks, loop = started.queue, started.loop

    loop.call_soon_threadsafe(tasks.put_nowait, ('abc', 5))
    loop.call_soon_threadsafe(tasks.put_nowait, ('def', 3))
    loop.call_soon_threadsafe(tasks.put_nowait, 'STOP')