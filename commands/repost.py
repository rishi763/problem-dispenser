from utils import problem_dict

async def repost(args, message, client):
    id=message.author.id
    problem=problem_dict.get(id)
    if problem is None:
        return await message.channel.send("You are not doing a problem at this moment.")
    return await message.channel.send(file=problem.get_image())