from utils import statistics
import discord

async def leaderboard(args, message, client):
    args=[x.lower() if type(x)==str else x for x in args]
    contests = {
        "aime": "AIME_RATING",
        "amc8":"AMC_8_RATING",
        "amc10": "AMC_10_RATING",
        "amc12": "AMC_12_RATING",
        "total":"TOTAL_RATING",
        "aime_solved":"AIME_SOLVED",
        "amc8_solved":"AMC_8_SOLVED",
        "amc10_solved":"AMC_10_SOLVED",
        "amc12_solved":"AMC_12_SOLVED",
        "total_solved":"TOTAL_SOLVED",
        "amc_8_solved":"AMC_8_SOLVED",
        "amc_10_solved":"AMC_10_SOLVED",
        "amc_12_solved":"AMC_12_SOLVED",
        "aimesolved":"AIME_SOLVED",
        "amc8solved":"AMC_8_SOLVED",
        "amc10solved":"AMC_10_SOLVED",
        "amc12solved":"AMC_12_SOLVED",
        "totalsolved":"TOTAL_SOLVED",
        "aime_rating": "AIME_RATING",
        "amc_8_rating":"AMC_8_RATING",
        "amc_10_rating": "AMC_10_RATING",
        "amc_12_rating": "AMC_12_RATING",
        "total_rating":"TOTAL_RATING"
    }
    name=0
    if len(args)==0:
        leaderboard_type="TOTAL_RATING"
        name=1
        number=1
    elif len(args)==1:
        try:
            number=int(args[0])
            leaderboard_type="TOTAL_RATING"
        except ValueError:
            number=1
            leaderboard_type=contests.get(args[0],"TOTAL_RATING")
    else:
        leaderboard_type=contests.get(args[0],"TOTAL_RATING")
        try:
            number=int(args[1])
        except:
            number=1
    if len(args)>0 and type(args[-1])==discord.TextChannel:
        channel=args[-1]
    else:
        channel=message.channel
    format_leaderboard=""
    leaderboard=statistics.get_leaderboard(leaderboard_type)
    if (number-1)*10>=len(leaderboard):
        number=1
    if number<=0:
        number=(len(leaderboard)-1)//10+1
    for i in range(10*(number-1),min(10*number,len(leaderboard))):
        format_leaderboard+=("`"+str(i+1)+"."+"` "+str(get_name(leaderboard[i][0], client))+" : "+str(leaderboard[i][1])+"\n").format(message)
    if leaderboard!=-1:
        if name==1:
            embed=discord.Embed(title="Leaderboard",description="Leaderboard for TOTAL_RATING",color=0x00ffb3)
            embed.add_field(name="TOTAL_RATING (Page "+str(number)+")",value=format_leaderboard)
        else:
            embed=discord.Embed(title="Leaderboard",description="Leaderboard for "+leaderboard_type,color=0x00ffb3)
            embed.add_field(name=leaderboard_type+" (Page "+str(number)+")",value=format_leaderboard)
        return await channel.send(embed=embed)
    return await channel.send("There was an error while displaying the leaderboard, please contact <@!513126047978356736> about this.")

def get_name(id, client):
    if client.get_user(id) is not None:
        user=client.get_user(id)
        statistics.set_name(id,user.name,user.discriminator)
        return user.name+"#"+user.discriminator
    elif statistics.get_cached_name(id) is not None:
        return statistics.get_cached_name(id)
    else:
        return None