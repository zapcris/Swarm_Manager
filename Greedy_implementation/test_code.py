from time import sleep
from queue import Queue
from threading import Thread


END = object()


def feed(queue: Queue):
    for i in range(10):
        print(f"Producing item {i}")
        sleep(0.5)
        queue.put(i)
    queue.put(END)


def dispatch(q_in: Queue, qs_out: list[Queue]):
    while True:
        item = q_in.get()

        if item is END:
            for q_out in qs_out:
                q_out.put(END)
            break

        for q_out in qs_out:
            q_out.put(item)


def process(item: int):
    sleep(0.5)
    print(f"Processed item {item}")


def worker(q_in: Queue):
    while True:
        item = q_in.get()
        if item is END: break
        process(item)


def main():
    q_in = Queue(maxsize=1)
    qs_out = [Queue(maxsize=1) for _ in range(3)]

    threads: list[Thread] = []

    threads.append(Thread(target=feed, args=(q_in,)))
    threads.append(Thread(target=dispatch, args=(q_in, qs_out)))

    for q_out in qs_out:
        threads.append(Thread(target=worker, args=(q_out,)))

    for t in threads: t.start()
    for t in threads: t.join()


if __name__ == "__main__":
    main()
