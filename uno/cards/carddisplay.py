import discord
from discord.ext import commands

sets = ['r','y','g','b']
chards = ['0','1','2','3','4','5','6','7','8','9','s','r','+']
uards = ['w','+','b']


prefix = '>'

description = 'The least wanted Bot.'
bot = commands.Bot(command_prefix=prefix, description=description)

@bot.event
async def on_ready():
    print("Client logged in")
    global msgs
    msgs = []

@bot.event
async def on_message(message):
    if message.content.startswith('>') or message.author == bot.user:
        msgs.append(message)
        if len(msgs) > 5:
            msgs.pop(0)
    await bot.process_commands(message)
    
@bot.command()
async def cards():
    for s in sets:
        for c in chards:
            image = s + c + '.png'
            await bot.send_file(msgs[len(msgs)-1].channel, image)
    for u in uards:
        image = 'u' + u + '.png'
        await bot.send_file(msgs[len(msgs)-1].channel, image)


bot.run("MzM3OTcwMTkwOTIwODQzMjY1.DFOo1w.a3ryM-TiaDJfTQ66oNvMAhFDWFg")
