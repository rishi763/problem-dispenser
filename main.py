import discord
from handlers.command_handler import command_handler
from utils.discord_helper import send_message
from dotenv import dotenv_values


config=dotenv_values(".env")
intents = discord.Intents.default()
#intents.members = True
#intents.messages=True
client = discord.Client(intents=intents)
reaction_messages=[]
is_reaction=False



@client.event
async def on_ready():
    game = discord.Game("with math | ?help | ?privacy for Privacy Policy")
    await client.change_presence(activity=game) 
    print(len(client.guilds),len(set(client.get_all_members())))
    print("LOGIN SUCCESSFUL")

@client.event
async def on_message(message):
    global client
    global is_reaction

    if message.author==client.user and len(message.embeds)==1 and message.embeds[0].title=="Leaderboard":
            await message.add_reaction("⬅️")
            await message.add_reaction("➡️")
            if len(reaction_messages)==100:
                reaction_messages.pop(0)
            reaction_messages.append([message,["leaderboard", message.embeds[0].fields[0].name.split()[0].lower(), int(message.embeds[0].fields[0].name.split()[-1][:-1].lower())]])
            return
    if message.author.bot:
        return
    # elif  type(message.content)==str and len(message.content)>1 and message.content[0]==";" and message.guild.id==813797379202613278:
    #     await command_handler(message.content[1:].lower().split(), message, client)
    # elif  type(message.content)==str and len(message.content)>1 and message.content.startswith("korn") and message.guild.id==696768410016809001:
    #     await command_handler(message.content[4:].lower().split(), message, client)
    elif type(message.content)==str and len(message.content)>1 and message.content[0]=="?":
        if message.content[1:].lower().split()[0]=="latex":
            await send_message(command_handler(message.content[1:].split(), message.author), message)
        else:
            await send_message(command_handler(message.content[1:].lower().split(), message.author), message)
    elif type(message.content)==str and message.content.count("$")>=2:
        await send_message(command_handler(["latex"]+message.content.split(), message.author), message)
    # elif type(message.content)==str and message.content.count("$")>=2:
    #     await command_handler(["latex"]+message.content.split(), message, client)
@client.event   
async def on_message_edit(before, after):
    #print(after)
    if after.author.bot:
        return
    if(type(after.content)==str) and len(after.content)>1 and after.content[0]=="?":
        await send_message(command_handler(after.content[1:].split(),after,client), after)

@client.event
async def on_reaction_add(reaction, user):
    
    if user==client.user:
        return
    if reaction.message in [x[0] for x in reaction_messages]:
        reaction_message=reaction_messages[[x[0] for x in reaction_messages].index(reaction.message)]
        if reaction_message[1][0]=="leaderboard":
            if reaction.emoji=="➡️":
                reaction_message[1][2]+=1
            elif reaction.emoji=="⬅️":
                reaction_message[1][2]-=1
            channel=reaction_message[0].channel
            await reaction_message[0].delete()
            reaction_messages.remove(reaction_message)
            await send_message(command_handler(reaction_message[1]+[channel],reaction_message[0].author), reaction_message[0])
client.run(config["TOKEN"])

