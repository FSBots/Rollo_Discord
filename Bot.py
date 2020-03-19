import discord
from discord.ext import commands
from Rollo import Rollo

client = commands.Bot(command_prefix='-')

@client.event
async def on_ready():
    print('Rollo Ready! <3')

@client.command(aliases=['tiro','arronza','rolla'])
async def roll(ctx,*,expression):
    try:
        rollo = Rollo()
        rollo.parse(expression)
    except:
        await ctx.send("cu o' cazzo")
    await ctx.send(rollo.getResultString())
    



client.run('')
#rollo = Rollo()
##rollo.parse("tira (3D1  +4) vantaggio")
#print("______________________________________")
