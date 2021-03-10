@client.command()
@commands.has_role('Bot Manager')
async def shell(ctx, * , command = None):
    if command == None:
        await missingArguments(ctx, "shell echo 'hello!'")
    timestamp = datetime.now()
    author = ctx.message.author
    guild = ctx.message.guild
    output = ""
    try:
        p = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        output += p.stdout
        embed = discord.Embed(title = "Shell Process", description = f"Shell Process started by {author.mention}", color = 0x4c594b)
        num_of_fields = len(output)//1014 + 1
        for i in range(num_of_fields):
            embed.add_field(name="Output" if i == 0 else "\u200b",  value="```bash\n" + output[i*1014:i+1*1014] + "\n```")
        embed.set_footer(text=guild.name + " | Date: " + str(timestamp.strftime(r"%x")))
        await ctx.send(embed = embed)
    except Exception as error:
        tb = error.__traceback__
        etype = type(error)
        exception = traceback.format_exception(etype, error, tb, chain=True)
        exception_msg = ""
        for line in exception:
            exception_msg += line
        embed = discord.Embed(title = "Shell Process", description = f"Shell Process started by {author.mention}", color = 0x4c594b)
        num_of_fields = len(output)//1014 + 1
        for i in range(num_of_fields):
            embed.add_field(name="Output" if i == 0 else "\u200b",  value="```bash\n" + exception_msg[i*1014:i+1*1014] + "\n```")
        embed.set_footer(text=guild.name + " | Date: " + str(timestamp.strftime(r"%x")))
        await ctx.send(embed = embed)
