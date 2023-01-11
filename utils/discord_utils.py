import discord
from dotenv import dotenv_values

config = dotenv_values(".env")
intents = discord.Intents.default()
client = discord.Client(intents=intents)


def get_name(id):
    if client.get_user(id) is not None:
        user = client.get_user(id)
        statistics.set_name(id, user.name, user.discriminator)
        return user.name+"#"+user.discriminator
    elif statistics.get_cached_name(id) is not None:
        return statistics.get_cached_name(id)
    else:
        return None
