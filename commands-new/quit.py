from utils import problem_dict
from utils import statistics
import time

def quit(args, author):
    id=author.id
    problem=problem_dict.get(id)
    if problem is None:
        return [{"text":"You are not doing a problem at this moment."}]
    problem.attempts=0
    statistics.update_values(id, problem.rating_updates(), author.name, author.discriminator)
    problem_dict.remove(id)
    time_taken=int(time.time()-problem.start_time)
    return [{"text":("You have quit this problem and took {} seconds, below is some information about it\n".format(time_taken)+"Source: {problem.path}\n"+("" if problem.answer is None else "Answer: ||{problem.answer}||\n")+("" if problem.urls["forum"] is None else "Forum Link: {problem.urls[forum]}\n")+("" if problem.urls["wiki"] is None else "Wiki Link: {problem.urls[wiki]}\n")).format(problem=problem)}]
