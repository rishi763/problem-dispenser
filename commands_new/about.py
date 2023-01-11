import discord

def about(args, author):
    return [{"text":"https://discord.gg/QMKh67c", "embed":discord.Embed(title="About Problem Dispenser",description="Problem Dispenser is a bot made by `Hoi#0913` to help mathletes improve their competitive math skills by practicing problems. It was made for myself but has grew to being used in {} servers. If you are looking for a math community to help you as you work through these problems be sure to join the server linked below:".format(str(len(client.guilds))),color=0x00ffb3)}]