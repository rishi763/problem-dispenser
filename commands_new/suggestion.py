async def suggestion(args, author):
    if len(args)==0:
        return -1
    suggestion_writer=open("data/suggestions.txt" ,'a')
    suggestion_writer.write(str(author)+":"+" ".join(args)+'\n')
    suggestion_writer.close()
    return [{"text":"Thanks for the suggestion, hopefully it will be implemented soon!"}]