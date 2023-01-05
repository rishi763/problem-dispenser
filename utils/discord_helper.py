import discord 
import json

async def send_message(json_data, message):
    for msg_data in json_data:
        text=msg_data.get("text", None)
        file=msg_data.get("file", None)
        files=msg_data.get("files", None)
        embed=msg_data.get("embed", None)
        time_skip=msg_data.get("time-skip", 0)
        dm=msg_data.get("dm", False)
        channel=msg_data.get("channel", None)
        if dm==True:
            await message.author.send(text, file=discord.File(file), files=[discord.File(file) for file in files], embed=embed)
        elif channel is not None:
            await channel.send(text, file=discord.File(file), files=[discord.File(file) for file in files], embed=embed)
        else:
            await message.channel.send(text, file=discord.File(file), files=[discord.File(file) for file in files], embed=embed)
        await asyncio.sleep(time_skip)