import asyncio

async def Main(count):
    print('Main function run.')
    for i in range(1, count+1):
        print('Assigning loop for Client '+str(i)+'...')
        asyncio.ensure_future(Mini(i))
        print('Loop for Client '+str(i)+' assigned.')
        await asyncio.sleep(1)
    print('Loops created.')
    while True:
        print('Searching for new connections...')
        await asyncio.sleep(0.1)

async def Mini(number):
    print('Task number ' + str(number) + ' start.')
    while True:
        print('Handling Client '+str(number)+'...')
        await asyncio.sleep(0.1)

loop = asyncio.get_event_loop()
count = int(input('Number of Clients:\n'))
loop.create_task(Main(count))
loop.run_forever()
print('End of loop.')