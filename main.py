from time import sleep
from typing import List
import discord
from configparser import ConfigParser
from discord.ext import commands
import subprocess

description = '''An example bot to showcase the discord.ext.commands extension module'''
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def whitelist(ctx, *args):
    """Adds two numbers together."""
    try:
        message = ' '.join(args)
        cmd = f'''sudo screen -r mcs -X stuff "whitelist {message}^M"'''
        print(f"whitelist: {message}")
        process = subprocess.run(cmd, shell=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        await ctx.send(f"Command error: {e}")
        return

    if process.returncode == 0:
        sleep(1)
        log = subprocess.run("tail -1 ../../minecraft/logs/latest.log", shell=True, capture_output=True)
        await ctx.send(log.stdout.decode())
        return
    
    msg = process.stdout if process.stdout != b'' else process.stderr if process.stderr != b''  else b''
    msg = msg.decode()
    if msg:
        await ctx.send(msg)
    else:
        await ctx.send(f"Command executed")

if __name__ == "__main__":

    config = ConfigParser()
    config.read("config.ini")
    bot.run(config['discord']['token'])