'''
SETUP:

This was orginally created toward REPL powered bots but now it should work for everything!

First, make sure your hosting platform is logged in with GIST/GitHub. You can login by trying to fetch a private repo on GitHub. 

Once you have done that, go inside the bot's folder and run these commands:

git fetch --all
git reset --hard origin/main

This should work if everything has been configured!
'''

async def force_restart(ctx):  #Forces the bot to apply changes to everything
    try:
        subprocess.run("python main.py", shell=True, text=True, capture_output=True, check=True)
    except Exception as e:
        await ctx.send(f"❌ Something went wrong while trying to restart the bot!\nThere might have been a bug which could have caused this!\n**Error:**\n{e}")
    finally:
        sys.exit(0)
        
        
        
 
#PLEASE DON'T COPY BOTH COMMANDS!
'''
One command assumes that you have the CogsManager commands imported while the other assumes you don't!
'''


@client.command()
async def gitpull(ctx, mode = "-a"): #CogsManager dependent!
    output = ''
      try:
          p = subprocess.run("git fetch --all", shell=True, text=True, capture_output=True, check=True)
          output += p.stdout
      except Exception as e:
          await ctx.send("⛔️ Unable to fetch the Current Repo Header!")
          await ctx.send(f"**Error:**\n{e}")
      try:
          p = subprocess.run("git reset --hard origin/main", shell=True, text=True, capture_output=True, check=True)
          output += p.stdout
      except Exception as e:
          await ctx.send("⛔️ Unable to apply changes!")
          await ctx.send(f"**Error:**\n{e}")
      embed = discord.Embed(title = "GitHub Local Reset", description = "Local Files changed to match PortalBot/Main", color = 0x3af250)
      embed.add_field(name = "Shell Output", value = f"```shell\n$ {output}\n```")
      embed.set_footer(text = "Attempting to restart the bot...")
      msg = await ctx.send(embed=embed)
      if mode == "-a":
          await force_restart(ctx)
      elif mode == "-c":
          await ctx.invoke(client.get_command('cogs reload'), ext='all') 
          
          
          
@client.command()
async def gitpull(ctx):
    output = ''
    BotName = '' #enter bot name here!
    try:
        p = subprocess.run("git fetch --all", shell=True, text=True, capture_output=True, check=True)
        output += p.stdout
    except Exception as e:
        await ctx.send("⛔️ Unable to fetch the Current Repo Header!")
        await ctx.send(f"**Error:**\n{e}")
    try:
        p = subprocess.run("git reset --hard origin/main", shell=True, text=True, capture_output=True, check=True)
        output += p.stdout
    except Exception as e:
        await ctx.send("⛔️ Unable to apply changes!")
        await ctx.send(f"**Error:**\n{e}")
    embed = discord.Embed(title = "GitHub Local Reset", description = f"Local Files changed to match {BotName}/Main", color = 0x3af250)
    embed.add_field(name = "Shell Output", value = f"```shell\n$ {output}\n```")
    embed.set_footer(text = "Attempting to restart the bot...")
    msg = await ctx.send(embed=embed)
    await force_restart(ctx)
