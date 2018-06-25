import multiprocessing
import time
import urllib.request
import lib104

def write(command):
    # req = urllib.request.Request("http://192.168.56.1:8081/write.json?tag=Devices.dev1.I1&val=777")
    req = urllib.request.Request("http://192.168.56.1:8081/write.json?tag=Devices.dev1.Open&val=1")
    res = urllib.request.urlopen(req)
    return res.read()


def handler(e, v, inputs):
    for input in inputs:
        print("Wait for event: Starting", input)
        time.sleep(1)
        print("Writing")
        print("Test Value now ---- ", id(v.value), v)
        write("Hello")
        e.wait()
        if e.is_set():
            print("Event catching!")
            print("Test Value now(2) ---- ", v.value)
        e.clear()


def worker(event, value):
    client = lib104.Client("192.168.56.1", 2404, event, value)
    time.sleep(2)
    client.run()
    while client.b_run:
        time.sleep(1)
        print("Client is running")
        # event.set()
        print("finish")


def main():
    print("Main")
    inputs = list(range(10))
    e = multiprocessing.Event()
    v = multiprocessing.Value('i', 0)
    http_sender_thread = multiprocessing.Process(
        name="waiter",
        target=handler,
        args=(e, v, inputs),
    )

    client_thread = multiprocessing.Process(
        name="Client",
        target=worker,
        args=(e, v,),
    )
    http_sender_thread.start()
    client_thread.start()
    client_thread.join()


if __name__ == "__main__":
    main()
