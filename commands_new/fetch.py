import os
from problem.problem import Problem
import json

def fetch(args, author):
    if args[0].replace("/","").isalnum() and os.path.exists("data/problems/{}/info.json".format(args[0].upper())):
        try:
            args=args[0].upper()
            year=int(args[:4])
            contest=None
            contests=json.load(open("problem/contests.json","r"))
            for test in contests:
                if test in args[5:]:
                    contest=test
                    break
            else:
                return [{"text":"Error!"}]
            version="None"
            if len(args.split('/'))>3:
                version=args.split('/')[2].replace((contest.split('/')+[""])[1],"")
            number=int(args.split('/')[-1])
            problem=Problem(dict={"year":year,"contest":contest,"version":version,"number":number})
            return [{"text":("Source: {problem.path}\n"+("" if len(problem.latex)>1800 else "Latex: ```{problem.latex}```\n")+("" if problem.answer is None else "Answer: ||{problem.answer}||\n")+("" if problem.urls["forum"] is None else "Forum Link: {problem.urls[forum]}\n")+("" if problem.urls["wiki"] is None else "Wiki Link: {problem.urls[wiki]}\n")).format(problem=problem),"file":problem.get_image()}]
        except:
            return [{"text":"Error!"}]
    else:
        return [{"text":"Invalid format."}]