from commands import *
from utils import problem_dict
from problem.problem  import Problem
import pickle
import random

SPECIAL_USERS=[513126047978356736, 639969433196036117, 447830705993678850, 669342948776738816]
ADMIN_USERS=[513126047978356736]

commands={
    "about": about.about,
    "ad": ad.ad,
    "ans": answer.answer,
    "answer": answer.answer,
    "fetch": fetch.fetch,
    "help": help.help,
    "inv": invite.invite,
    "invite": invite.invite,
    "latex":latex.latex,
    "lb":leaderboard.leaderboard,
    "leaderboard":leaderboard.leaderboard,
    "mock": mock.mock,
    "privacy": privacy.privacy,
    "quit": quit.quit,
    "repost": repost.repost,
    "settings": settings.settings,
    "statistics":statistics.statistics,
    "stats": statistics.statistics,
    "suggest": suggestion.suggestion,
    "suggestion": suggestion.suggestion
}

special_commands={
    
}

admin_commands={
    
}
def invalid_command(args, author):
    return None

def command_handler(args, author):
    allowed_cmds=commands|(special_commands if author.id in SPECIAL_USERS else {})|(admin_commands if author.id in ADMIN_USERS else {})
    #if author.id not in pickle.load(open("data/voters.pickle","rb")) and random.randint(1,15)==3:
        #await message.channel.send("Hey it seems like to use this bot! You should go to Math Club ( https://discord.gg/QMKh67c ) and register to vote using `?register` so I, <@!513126047978356736>, can regain my role as Board Member. (Once you register you will not see this message again.)")
    msg_data=allowed_cmds.get(args[0],invalid_command)(args[1:], author)
    if msg_data is None:
        problem=Problem(args=" ".join(args).lower())
        if not problem.valid:
            return None
        else:
            if problem_dict.get(author.id) is not None:
                return [{"text":"You are already doing a problem.", "file": problem_dict.get(author.id).get_image()}]
            else:
                problem_dict.add(author.id, problem)
                return [{"file":problem.get_image()}]
    else:
        return msg_data

#send args+author