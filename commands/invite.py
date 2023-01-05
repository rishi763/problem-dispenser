async def invite(args, message, client):
    return await message.channel.send("https://discord.com/api/oauth2/authorize?client_id=721372133564874793&permissions=59456&scope=bot")