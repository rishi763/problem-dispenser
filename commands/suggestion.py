async def suggestion(args, message, client):
    if len(args)==0:
        return -1
    suggestion_writer=open("data/suggestions.txt" ,'a')
    suggestion_writer.write(str(message.author)+":"+" ".join(args)+'\n')
    suggestion_writer.close()
    return await message.channel.send("Thanks for the suggestion, hopefully it will be implemented soon!")