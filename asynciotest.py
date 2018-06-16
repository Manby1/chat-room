import asyncio

response = 0

async def handle(x):
    return x

async def run():
    global response
    for number in range(1, 21):
        response = await handle(number)
        print(response)
        if response == 10:

            # run wait_for_next "in background" instead of blocking flow:
            asyncio.ensure_future(wait_for_next(response))

async def wait_for_next(x):
    while response == x:
        print('waiting',response,x)
        await asyncio.sleep(0.5)
    print('done')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())