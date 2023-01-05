import discord
import pickle

async def vote(args, message, client):
    voters=candidates=None
    with open("data/voters.pickle", "rb") as voters_file:
        voters=pickle.load(voters_file)
    with open("data/candidates.pickle", "rb") as candidates_file:
        candidates=pickle.load(candidates_file)
    args=" ".join(args).lower()
    if not isinstance(message.channel, discord.channel.DMChannel):
        await message.channel.send("Please vote in DMs, your votes need to be private!!!")
        return await message.delete()        
    if message.author.id in voters:
        if len(voters[message.author.id])==5:
            return await message.channel.send("Sorry you have voted too many times, please contact <@!513126047978356736> if you want to change your votes asap!!!")
        for name in candidates:
            if name in args.lower():
                if name in voters[message.author.id]:
                    return await message.channel.send("You have voted for this candidate already, please vote for someone else or not at all.")
                voters[message.author.id].append(name)
                candidates[name]+=1
                embed=discord.Embed(title="Election", description="The current vote tallys in the 3rd semester 2020-2021 Math Club elections",color=0x00ffb3)
                for candidate in candidates:
                    embed.add_field(name=candidate, value="`{}` | {} votes".format("█"*(candidates[candidate])+" "*(30-candidates[candidate]),candidates[candidate]))
                await client.get_channel(796131010181070898).send(embed=embed)
                pickle.dump(voters, open('data/voters.pickle' , 'wb'))
                pickle.dump(candidates, open('data/candidates.pickle' , 'wb'))
                return await message.channel.send("Congrats you have voted for {}, you have {} votes remaining to use".format(name, 5-len(voters[message.author.id])))
        return await message.channel.send("Sorry that is not a valid candidate, please try again.")
    return await message.channel.send("Sorry, but you are not registered to vote, please contact <@!688411789180141603> for any last minute changes")
