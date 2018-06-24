import asyncio

response = 0

async def handle(x):
    await asyncio.sleep(0.1)
    return x

async def run():
    global response
    for number in range(1, 21):
        response = await handle(number)
        print(response)
        if response == 10:

            # run wait_for_next "in background" instead of blocking flow:
            task = loop.create_task(wait_for_next(response))
            tasks.append(task)

async def wait_for_next(x):
    while response == x:
        print('waiting',response,x)
        await asyncio.sleep(0.5)
    print('done')


tasks = [run()]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))