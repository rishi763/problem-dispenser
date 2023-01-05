import discord
import pickle

async def register(args, message, client):
    try: 
        voters=pickle.load(open("data/voters.pickle", "rb"))
    except:
        voters=[]
    try:
        await client.get_guild(696768410016809001).fetch_member(message.author.id)
    except:
        return await message.channel.send("You need to be in Math Club to register to vote.")
    if message.author.id not in voters:
        voters.append(message.author.id)
        member=await client.get_guild(696768410016809001).fetch_member(message.author.id)
        await member.add_roles(discord.utils.get(client.get_guild(696768410016809001).roles,name="Registered Voter"))
        pickle.dump(voters, open("data/voters.pickle", "wb"))
        return await message.channel.send("You have been successfully registered to vote.")
    else:
        return await message.channel.send("You have already registered to vote.")
