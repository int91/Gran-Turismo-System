from turtle import pos
import globals as g
import nextcord
from nextcord.ext import commands
import numpy.random
import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv
import sql
import bot_commands

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

prefixes = [";", "inv", "v ", "v", "i"]

bot = commands.Bot(prefixes[0])
BOT_ID = 954533657022959648

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message_create(ctx):
    if (ctx.author.id == BOT_ID):
        return
    bot.process_commands(ctx.message)

@bot.command(name="register")
async def register(ctx, name: str):
    await bot_commands.Register(ctx, name)

@bot.command(name="q")
async def q(ctx):
    #await mining.Mine(ctx, oreId)
    pass

@bot.command(name="result")
async def result(ctx, raceId, userName: str, qualify: str, position: str):
    qualify = int(qualify)
    position = int(position)
    await bot_commands.RaceResult(ctx, raceId, userName, qualify, position)


@bot.command(name="name")
async def name(ctx, discordId: str):
    await bot_commands.GetName(ctx, discordId)

def Main():
    sql.ConnectToDB()
    #botThread = threading.Thread(target=bot.run, args=[os.getenv("BOT_TOKEN")])
    #botThread.start()
    #botThread.join()
    bot.run(os.getenv("BOT_TOKEN"))
    sql.CloseConnectionToDB()

if __name__ == "__main__":
    numpy.random.seed(int(datetime.datetime.utcnow().timestamp()))
    Main()