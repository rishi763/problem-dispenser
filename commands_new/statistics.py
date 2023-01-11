from utils import statistics as stats_utils
import discord

def statistics(args, author):
    if len(args)==0:
        id=author.id 
    elif len(message.mentions)!=0:
        id=message.mentions[0].id
    elif stats_utils.user_exists(args[0]):
        id=int(args[0])
    else:
        id=stats_utils.get_user_id(args[0].split('#')[0], args[0].split('#')[1])
    embed=discord.Embed(title=("Statistics"), description=("Statistics for {} on Problem Dispenser").format(get_name(id, client)), color=0x00ffb3)   
    user_stats=stats_utils.get_stats(id)
    if user_stats is not None: 
        embed.add_field(name="Problem Solved", value="`AMC 8` `{}` `#{}`\n`AMC10` `{}` `#{}`\n`AMC12` `{}` `#{}`\n`AIME ` `{}` `#{}`\n`CALT ` `{}` `#{}`\n` SMC ` `{}` `#{}`\n`TOTAL` `{}` `#{}`".format(*user_stats[0:14]))
        embed.add_field(name="Problem Failed", value="`AMC 8` `{}`\n`AMC10` `{}`\n`AMC12` `{}`\n`AIME ` `{}`\n`CALT ` `{}`\n` SMC ` `{}`\n`TOTAL` `{}`".format(*user_stats[14:21]))
        embed.add_field(name="Rating", value="`AMC 8` `{}` `#{}`\n`AMC10` `{}` `#{}`\n`AMC12` `{}` `#{}`\n`AIME ` `{}` `#{}`\n`TOTAL` `{}` `#{}`".format(*user_stats[21:]))
        return [{"embed":embed}]
    return [{"text":"This user hasn't solved any problems yet!"}]

def get_name(id, client):
    if client.get_user(id) is not None:
        user=client.get_user(id)
        stats_utils.set_name(id,user.name,user.discriminator)
        return user.name+"#"+user.discriminator
    elif stats_utils.get_cached_name(id) is not None:
        return stats_utils.get_cached_name(id)
    else:
        return None