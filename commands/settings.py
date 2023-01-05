import discord
from utils import statistics

async def settings(args, message, client):
    if len(args)==0 or args[0].lower()!="public":
        embed=discord.Embed(title="Settings for {}".format(message.author.name+"#"+message.author.discriminator),color=0x00ffb3)
        embed.add_field(name="Public: {}".format(statistics.get_public(message.author.id)),value="This setting allows you to be shown on the leaderboard")
        return await message.channel.send(embed=embed)
    elif len(args)>1 and args[1].lower() in ["true","false"]:
        if args[1].lower()=="true":
            statistics.set_public(message.author.id,True)
            return await message.channel.send("Successfully changed Public to True")
        else:
            statistics.set_public(message.author.id,False)
            return await message.channel.send("Successfully changed Public to False")