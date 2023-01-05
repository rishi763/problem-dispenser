import discord

async def help(args, message, client):
    args=[x.lower() for x in args]
    commands={
        "about":["Information about `?about`","This gives a brief overview of the bot, it does not have any parameters."],
        "aime":["Information about `AIME`","Some general info about what the bot can do with this contest.","`Aliases`","There are no aliases for this contest","`General Info`","The AIME can be answered and there are links to solutions","`More Info`","https://artofproblemsolving.com/wiki/index.php/American_Invitational_Mathematics_Examination"],
        "amc10":["Information about `AMC 10`","Some general info about what the bot can do with this contest.","`Aliases`","`amc 10`","`General Info`","The AMC 10 can be answered and there are links to solutions","`More Info`","https://artofproblemsolving.com/wiki/index.php/AMC_10"],
        "amc12":["Information about `AMC 12`","Some general info about what the bot can do with this contest.","`Aliases`","`amc 12`","`General Info`","The AMC 12 can be answered and there are links to solutions","`More Info`","https://artofproblemsolving.com/wiki/index.php/AMC_12"],
        "answer":["Information about `?answer [ANSWER]`","This is the way you answer the problem you are working on.","`Aliases`","`ans`","`[ANSWER]` is a needed parameter","It can be a 3-digit integer number for AIME problems or a letter for AMC problems."],
        "calt":["Information about `CALT`","Some general info about what the bot can do with this contest.","`Aliases`","There are no aliases for this contest.","`General Info`","The CALT can be answered but there are no links to solutions","`More Info`","https://thecalt.com/"],
        "difficulty":["Information about `?difficulty`","Some information about the different difficulties","`EASY`","The aliases for this difficulty are `e` and `ez`","`MEDIUM`","The aliases for this difficulty are`m`, `med` and `moderate`","`HARD`","The alias for this difficulty is `h`"],
        "fetch":["Information about `?fetch (PATH)`","This lets you fetch any problem that Problem Dispenser has.","`PATH` is a needed parameter","Path is the location of the problem you are searching for, it must be in the format `YEAR/CONTEST/VERSION/NUMBER`"],
        "invite":["Information about `?invite`","This sends a link to invite this bot to your server :)."],
        "help":["Information about `?help (COMMAND)`","This gives information about each command.","`(COMMAND)` is an optional parameter","It can be any of the commands shown here, but it defaults to showing the general help menu","`HMMT`","HMMT contests along with answers should be added soon, and maybe solutions too!!!"],
        "hmmt":["Information about `HMMT`","Some general info about what the bot can do with this contest.","`Aliases`","There are no aliases for this contest","`General Info`","HMMT cannot be answered and there are not any links to solutions", "`CATEGORIES`","`Advanced`, `Algebra`, `Calculus`,`Combinatorics`,`General`,`Geometry`,`Guts`,`Oral`,`Team`,`November General`,`November Guts`,`November Team`,`November Theme`","`More Info`","https://www.hmmt.org/www/tournaments/novfeb"],
        "leaderboard":["Information about `?leaderboard (CONTEST) (PAGE)`","This displays the leaderboard for this bot with various options.","`Aliases`","`lb`","`(CONTEST)` is an optional parameter","It can be either AMC10, AMC12, AIME, or Overall, but it defaults to Overall.","`(PAGE)` is a optional parameter.","This is the page number of the leaderboard and it can be any integer, but it defaults to the first page."],
        "problem":["Information about `?[CONTEST] (DIFFICULTY) (CATEGORY)`","This gives you a problem to work on!","`[CONTEST]` is an needed parameter","The contests that we currently have are `AMC 10`,`AMC 12`,`AIME`,`CALT`,`HMMT`,`SMC`,`USAJMO`,`USAMO` (do `?help[CONTEST]` for more info)","`(DIFFICULTY)` is a optional parameter.","This allows you to choose the difficulty of the problem you choose within a specific category (Do `?help difficulty` for more info).", "`(CATEGORY)` is a optional parameter.","This allows you to choose the specific category (Do `?help [CONTEST]` for more info)."],
        "repost":["Information about `?repost`","This reposts the problem you are currenly working on incase you can't find it and it takes no parameters."],
        "reset":["Information about `?reset (USER) [CONFIRMATION]`","This resets your statistics","`(USER)` is an optional parameter","It can be a ping of any username in that server, but it defaults to you","`[CONFIRMATION]` is a needed parameter." ,"This is a confirmation you want to delete your data."],
        "smc":["Information about `SMC`","Some general info about what the bot can do with this contest.","`Aliases`","There are no aliases for this contest.","`General Info`","The SMC can be answered but there are no links to solutions","`More Info`","https://sacramentomathcommunity.ml/"],
        "statistics":["Information about `?statistics (USER)`","This gives the statistics of the user selected","`Aliases`","`stats`","`(USER)` is an optional parameter","It can be a ping of any username in that server, but it defaults to you."],
        "suggestion":["Information about `?suggestion [SUGGESTION]`","This allows you to say what you want/think should be added to this bot", "`[SUGGESTION]` is a needed parameter","It can be anything you want to say :)"],
        "quit":["Information about `?quit`","This quits the problem you are working on and takes no additional parameters."],
        "usajmo":["Information about `USAJMO`","Some general info about what the bot can do with this contest.","`Aliases`","`JMO`","`General Info`","The USAJMO cannot be answered but there are links to solutions","`More Info`","https://artofproblemsolving.com/wiki/index.php/United_States_of_America_Junior_Mathematical_Olympiad"],
        "usamo":["Information about `USAMO`","Some general info about what the bot can do with this contest.","`Aliases`","`AMO`","`General Info`","The USAMO cannot be answered but there are links to solutions","`More Info`","https://artofproblemsolving.com/wiki/index.php/United_States_of_America_Mathematical_Olympiad"]
        }
    if len(args)==0:
        embed=discord.Embed(title="Commands for Problem Dispenser",description="Do `?help [COMMAND]` to get more in-depth info about each command!",color=0x00ffb3)
        embed.add_field(name="`?problem`", value="This gives you a problem to solve. Please look at `?help problem` for more info.")
        embed.add_field(name="`?about`", value="Gives a brief overview of the bot ")
        embed.add_field(name="`?answer`", value="This allows you to answer questions given.")
        embed.add_field(name="`?fetch`", value="This allows you to get info about a certain problem")
        embed.add_field(name="`?help`", value="This is the help command for this bot.")
        embed.add_field(name="`?invite`", value="This sends an invite link for this bot")
        embed.add_field(name="`?leaderboard`", value="This displays the global leaderboard based on problems solved.")
        embed.add_field(name="`?repost`", value="This reposts the problem you are currently working on")
        embed.add_field(name="`?reset`", value="This resets your statistics.")
        embed.add_field(name="`?statistics`", value="This shows your statistics.")
        embed.add_field(name="`?suggestion`", value="This allows you to give feedback/suggestions.")
        embed.add_field(name="`?quit`", value="This quits the current problem you are working on.")
        return await message.channel.send(embed=embed)
    embed_details=commands.get(args[0], None)   
    if embed_details is not None:
        embed=discord.Embed(title=embed_details[0], description=embed_details[1], color=0x00ffb3)
        i=2
        while i<len(embed_details):
            embed.add_field(name=embed_details[i], value=embed_details[i+1])
            i+=2
        return await message.channel.send(embed=embed)
    return await help([], message, client)