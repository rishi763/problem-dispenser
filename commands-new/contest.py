import asyncio
import discord
import os
import json
import subprocess
from problem.problem import Problem

TEMPLATE="\\documentclass[12pt]{{article}}\r\n\\usepackage{{asymptote}}\r\n\\usepackage{{amsmath}}\r\n\\usepackage{{amssymb}}\r\n\\usepackage{{amsfonts}}\r\n\\usepackage{{enumitem}}\r\n\\usepackage{{graphicx}}\r\n\\begin{{document}}\r\n\\begin{{enumerate}}\r\n\r\n{}\r\n\\end{{enumerate}}\r\n\\end{{document}}"

def contest(args, author):
    path=args[0].upper()
    if path.replace("/","").isalnum() and os.path.exists("data/problems/{}".format(path)) and os.path.isdir("data/problems/{}".format(path)) and os.path.isdir("data/problems/{}/{}".format(path, os.listdir("data/problems/{}".format(path))[0])) and os.path.isfile("data/problems/{}/{}/info.json".format(path, os.listdir("data/problems/{}".format(path))[0])):
        year=int(path[:4])
        contest=None
        contests=json.load(open("problem/contests.json", "r"))
        for item in contests:
            if item in path:
                contest=item
                break
        else:
            return [{"text":"Error!"}]
        version="None"
        if path.replace(str(year),"").replace(contest, "").replace("/","")!="":
            version=path.replace(str(year),"").replace(contest, "").replace("/","")
        max=0
        for number in os.listdir("data/problems/{}".format(path)):
            if int(number)>max:
                max=int(number)
                problems=[Problem(dict={"year":year,"contest":contest,"version":version,"number":i}) for i in range(1,max+1)]
        for file in os.listdir("latex/contest"):
            if file.endswith(".asy") or file.endswith(".pdf"):
                os.remove("latex/contest/{}".format(file))
        with open("latex/contest/contest.tex", "w") as contest_writer:
            problems_string=""
            for problem in problems:
                problems_string+="\\item {}\r\n".format(problem.latex)
            contest_writer.write(TEMPLATE.format(format_latex(problems_string)))
        subprocess.run("pdflatex -interaction=nonstopmode -output-directory=latex/contest contest.tex".split(" "))
        for i in range(1,len([file for file in os.listdir("latex/contest") if file.endswith(".asy")])+1):
            subprocess.run("asy --cd=latex/contest contest-{}.asy".format(i).split(" "))
        subprocess.run("pdflatex -interaction=nonstopmode -output-directory=latex/contest contest.tex".split(" "))
        files=[]
        if contests[contest]["answer"]:
            with open("latex/contest/answers.txt","w") as answers_file:
                answers_text="Answers to contest:\n"
                for i in range(len(problems)):
                    answers_text+="{}: {}\n".format(i+1, problems[i].answer)
                answers_file.write(answers_text)
                answers_file.flush()
            files.append("latex/contest/answers.txt")
        with open("latex/contest/links.txt", "w") as links_file:
            links_text="Links to contest:\n"
            for i in range(len(problems)): 
                links_text+="{}: {} {}\n".format(i+1, problems[i].urls["forum"], problems[i].urls["wiki"])
            links_file.write(links_text)
            links_file.flush()
        files.append("latex/contest/links.txt")
        return [{"text":"Here is your contest!", "file":"latex/contest/contest.pdf", "dm":True},{"text":"You will be sent answers(if applicable) and links to solutions in {} seconds".format(contests[contest]["time"]), "time-skip":contests[contest]["time"], "dm":True},{"text":"Here are the solutions!", "files":files, "dm":True}]
    else:
        return  [{"text":"Invalid format"}]

def format_latex(text):
    return remove_trailing(text.replace("defaultpen(white)","defaultpen(black)"))

def remove_trailing(text):
    if text.endswith("\\") or text.endswith("\n") or text.endswith("\r"):
        return remove_trailing(text[:-2])
    else:
        return text
