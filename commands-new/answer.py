from utils import problem_dict
from utils import statistics
import time


def answer(args, author):
    args=[x.upper() for x in args]
    id=author.id
    problem=problem_dict.get(id)
    if problem is None:
        return [{"text":"You are not doing a problem at this moment."}]
    if problem.answer is None:
        problem_dict.remove(id)
        time_taken=int(time.time()-problem.start_time)
        return [{"text":("You cannot answer this question at the moment but it took you {} seconds to solve this problem,".format(time_taken)+"look below to see if you can find an answer\nSource: {problem.path}\n"+("" if problem.answer is None else "Answer: ||{problem.answer}||\n")+("" if problem.urls["forum"] is None else "Forum Link: {problem.urls[forum]}\n")+("" if problem.urls["wiki"] is None else "Wiki Link: {problem.urls[wiki]}\n")).format(problem=problem)}]
    if args[0]==problem.answer:
        statistics.update_values(id, problem.rating_updates(), author.name, author.discriminator)
        problem_dict.remove(id)
        time_taken=int(time.time()-problem.start_time)
        return [{"text":("You got the right answer and took {} seconds!".format(time_taken)+" Below is some information about the problem\nSource: {problem.path}\n"+("" if problem.answer is None else "Answer: ||{problem.answer}||\n")+("" if problem.urls["forum"] is None else "Forum Link: {problem.urls[forum]}\n")+("" if problem.urls["wiki"] is None else "Wiki Link: {problem.urls[wiki]}\n")).format(problem=problem)}]
    else:
        problem_dict.lower_attempts(id)
        if problem.attempts>0:
            return [{"text":"You got the wrong answer, you have {} attempt{} left.".format(problem.attempts, ("s" if problem.attempts>1 else ""))}]
        else:
            statistics.update_values(id, problem.rating_updates(), author.name, author.discriminator)
            problem_dict.remove(id)
            return [{"text":("You got the wrong answer too many times, below is some information about the problem\nSource: {problem.path}\n"+("" if problem.answer is None else "Answer: ||{problem.answer}||\n")+("" if problem.urls["forum"] is None else "Forum Link: {problem.urls[forum]}\n")+("" if problem.urls["wiki"] is None else "Wiki Link: {problem.urls[wiki]}\n")).format(problem=problem)}]

