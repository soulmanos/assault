import asyncio
import time
import os
import requests

"""
We have one worker for each concurrent request we want to be able to make, 
but each worker will work its way through more than one request. 
To handle more than one request, we're going to run an infinite loop within 
each of our workers that will wait for a new item to be added to the queue.

The first thing that we're going to do is get the event loop that our current 
asynchronous code is running within. We're going to use this event loop 
within our while loop to asynchronously execute our fetch function.
Moving into the while loop, the first thing that we need to do is get the URL 
from the queue. Since our queue is designed to be used asynchronously, that 
means that when we call queue.get, we need to use the await keyword to say 
that we want to wait for a value to be returned to us. Then, we just have 
a little debug statement so that we can see which worker is making a request 
when we actually run this code.
Next, we're going to use loop.run_in_executor to take our fetch function 
and run it as a coroutine on our current event loop. This allows us to run 
a function that we know has some blocking code in it (such as a network 
request) on the event loop. The requests library isn't written to be used 
with asyncio, but running our fetch function on the event loop allows us 
to mostly get around that. We receive an asyncio.Future object from this 
function, which we can use await with to get the actual value back.
Lastly, we'll add the result to our results list, and then we get to mark the 
item from the queue as complete by calling queue.task_done(). By doing this, 
we let the queue know that the item was processed and it can be considered 
fully removed. This is important because when we called queue.join(), we were 
saying that we wanted to wait until this method has been called for every 
item that was in the queue.
"""


def fetch(url):
    """ Make the request and return the results """
    started_at = time.monotonic()
    response = requests.get(url)
    request_time = time.monotonic() - started_at
    return {"status_code": response.status_code, "request_time": request_time}


async def worker(name, queue, results):
    """ A function to take unmake requests from a queue and perform the work then add results to the results list """
    loop = asyncio.get_event_loop()
    while True:
        url = await queue.get()
        if os.getenv("DEBUG"):
            print(f"{name} - Fetching url {url}")
        # Allow us to run non-asyncio code on the event-loop, note we're passing the function 'fetch' not calling it
        # Returns a 'future' - Need this type of function because 'requests' isn't asyncio compatible
        future_result = loop.run_in_executor(None, fetch, url)
        result = await future_result
        results.append(result)
        queue.task_done()


async def distribute_work(url, requests, concurrency, results):
    """ Divide the work into batches and collect the final results """
    queue = asyncio.Queue()

    for _ in range(requests):
        queue.put_nowait(url)

    tasks = []
    for i in range(concurrency):
        task = asyncio.create_task(worker(f"worker-{i+1}", queue, results))
        tasks.append(task)

    started_at = time.monotonic()
    await queue.join()  # Wait until every item within the queue is finished
    total_time = time.monotonic() - started_at

    for task in tasks:
        task.cancel()

    return total_time
    # print("---")
    # print(
    #     f"{concurrency} workers took {total_time:.2f} seconds to complete {len(results)} requests"
    # )


def assault(url, requests, concurrency):
    """ Entrypoint to making requests """
    results = []
    total_time = asyncio.run(
        distribute_work(url, requests, concurrency, results)
    )  # distribute_work doesn't return result, but returns a coroutine, that asyncio.run() will cause to execute
    return (total_time, results)
    # print(results)
