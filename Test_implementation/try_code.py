# SuperFastPython.com
# example of using a sharedmemorymanager to manage a sharablelist
from multiprocessing import Process
from multiprocessing.managers import SharedMemoryManager


# task executed in a child process
def task(sl):
    # change the list
    for i in range(len(sl)):
        sl[i] = sl[i] * 10


# protect the entry point
if __name__ == '__main__':
    # create the manager
    manager = SharedMemoryManager()
    # start the manager
    manager.start()
    # create a shared list using the manager
    sl = manager.ShareableList([1, 2, 3, 4, 5])
    # report the shared list
    print(sl)
    # create a child process
    process = Process(target=task, args=(sl,))
    # start the child process
    process.start()
    # wait for the child process to finish
    process.join()
    # report the shared list
    print(sl)
    # shutdown the manager
    manager.shutdown()