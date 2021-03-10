from discord.ext import commands
import discord
from typing import List
import traceback
from pathlib import Path
import core.common
import asyncio
import requests
import yarl
import os
import json
from core.common import query
import logging
import random

logger = logging.getLogger(__name__)


'''
SETUP:
In order to use this error handler, you require an .env file with your GIST token! (Variable must be GIST) 
Ex:

GIST = to_k_en

You can create a GIST Token here:
https://github.com/settings/tokens/new

Guide:
https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

Scopes Required:
GIST

'''


def random_rgb(seed=None):
    if seed is not None:
        random.seed(seed)
    return discord.Colour.from_rgb(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))


def stackoverflow(q):
    q = str(q)
    baseUrl = "https://stackoverflow.com/search?q="
    error = q.replace(" ","+")
    error = error.replace(".","")
    stackURL = baseUrl + error 
    return stackURL

class GithubError(commands.CommandError):
    pass


class CustomError(Exception):
    def __init__(self, times: int, msg: str):
        self.times = times
        self.msg = msg
        self.pre = "This is a custom error:"
        self.message = f"{self.pre} {self.msg*self.times}"
        super().__init__(self.message)


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        logger.info("ErrorHandler: Cog Loaded!")

    @commands.command() #method of testing the error handler!
    async def error(self, ctx, times: int = 20, msg="error"):
        raise CustomError(int(times), msg)

        
        
    # Checks if the command has a local error handler.
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error: Exception):
        tb = error.__traceback__
        etype = type(error)
        exception = traceback.format_exception(etype, error, tb, chain=True) #Format the Exception so it includes every detail (line number, full stack traceback.
        exception_msg = ""
        sturl = stackoverflow(error)
        for line in exception: #Writes to a file so you can see the latest traceback. 
            exception_msg += line
        
        if isinstance(error, commands.CheckFailure) or isinstance(error, commands.CheckAnyFailure):
            return

        if hasattr(ctx.command, 'on_error'):
            return

        elif isinstance(error, commands.CommandNotFound):
            config, _ = core.common.load_config()
            print("Ignored error: " + str(ctx.command))
            return
        else:
            error_file = Path("error.txt") 
            error_file.touch()
            with error_file.open("w") as f:
                f.write(exception_msg)
            with error_file.open("r") as f:
                config, _ = core.common.load_config()
                data = "\n".join([l.strip() for l in f])

                GITHUB_API="https://api.github.com"
                API_TOKEN=os.getenv("GIST")
                url=GITHUB_API+"/gists"
                print(f"Request URL: {url}")                    
                headers={'Authorization':'token %s'%API_TOKEN}
                params={'scope':'gist'}
                payload={"description":"PortalBot encountered a Traceback!","public":True,"files":{"error":{"content": f"{data}"}}}
                res=requests.post(url,headers=headers,params=params,data=json.dumps(payload))
                j=json.loads(res.text)
                ID = j['id']
                #ID = j.ID
                gisturl = f"https://gist.github.com/{ID}"
                print(gisturl)

                embed = discord.Embed(title = "Beep Boop", description = "🚨 *I've ran into an issue!* 🚨\nThe Developers should get back to fixing that!", color = random_rgb())
                embed.add_field(name = "Gist URL", value = f"**https://gist.github.com/{ID}**")
                embed.add_field(name = "Stack Overflow", value = f"**{sturl}**", inline = False)
                embed.set_footer(text = f"Error: {str(error)}")
                await ctx.send(embed = embed)
                error_file.unlink()
                
         


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))

