import discord
from utils import statistics

def settings(args, author):
    if len(args)==0 or args[0].lower()!="public":
        embed=discord.Embed(title="Settings for {}".format(author.name+"#"+author.discriminator),color=0x00ffb3)
        embed.add_field(name="Public: {}".format(statistics.get_public(author.id)),value="This setting allows you to be shown on the leaderboard")
        return [{"embed":embed}]
    elif len(args)>1 and args[1].lower() in ["true","false"]:
        if args[1].lower()=="true":
            statistics.set_public(author.id,True)
            return [{"text":"Successfully changed Public to True"}]
        else:
            statistics.set_public(author.id,False)
            return [{"text":"Successfully changed Public to False"}]