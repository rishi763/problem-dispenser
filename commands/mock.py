import asyncio
import discord
import os
import subprocess
import json
from problem.problem import Problem
DIFFICULTIES=["ez","easy","med","medium","hard","insane"]
TEMPLATE="\\documentclass[12pt]{{article}}\r\n\\usepackage{{asymptote}}\r\n\\usepackage{{amsmath}}\r\n\\usepackage{{amssymb}}\r\n\\usepackage{{amsfonts}}\r\n\\usepackage{{enumitem}}\r\n\\usepackage{{graphicx}}\r\n\\begin{{document}}\r\n\\begin{{enumerate}}\r\n\r\n{}\r\n\\end{{enumerate}}\r\n\\end{{document}}"

async def mock(args, message, client):
    contest=Problem(" ".join(args).lower()).contest
    if contest not in ["AIME", "AMC/8", "AMC/10", "AMC/12", "USAJMO", "IMO"]:
        return await message.channel.send("You either forgot to mention a contest or the contest you chose is not supported at the moment.")
    await message.channel.send("Preparing mock...")
    for file in os.listdir("latex/mock"):
        if file.endswith(".asy") or file.endswith(".pdf"):
            os.remove("latex/mock/{}".format(file))
    
    with open("problem/contests.json", "r") as contests_file:
        contests=json.load(contests_file)
    problems=[0]*(len(contests[contest]["None"]["easy"])+len(contests[contest]["None"]["medium"])+len(contests[contest]["None"]["hard"]))
    for difficulty in DIFFICULTIES:
        if difficulty in args:
            for number in contests[contest]["None"]["easy"]+contests[contest]["None"]["medium"]+contests[contest]["None"]["hard"]:
                problems[number-1]=Problem(" ".join(args).lower()) 
                while problems[number-1] in problems[:number-1]:
                    problems[number-1]=Problem(" ".join(args).lower())
            break
    else:
        for number in contests[contest]["None"]["easy"]:
            problems[number-1]=Problem(" ".join(args).lower()+" easy")
            while problems[number-1] in problems[:number-1]:
                problems[number-1]=Problem(" ".join(args).lower()+" easy")
        for number in contests[contest]["None"]["medium"]:
            problems[number-1]=Problem(" ".join(args).lower()+" medium")
            while problems[number-1] in problems[:number-1]:
                problems[number-1]=Problem(" ".join(args).lower()+" medium")
        for number in contests[contest]["None"]["hard"]:
            problems[number-1]=Problem(" ".join(args).lower()+" hard")
            while problems[number-1] in problems[:number-1]:
                problems[number-1]=Problem(" ".join(args).lower()+" hard")
    with open("latex/mock/mock.tex", "w") as mock_writer:
        problems_string=""
        for problem in problems:
            problems_string+="\\item {}\r\n".format(problem.latex)
        mock_writer.write(TEMPLATE.format(format_latex(problems_string)))
    subprocess.run("pdflatex -interaction=nonstopmode -output-directory=latex/mock mock.tex".split(" "))
    for i in range(1,len([file for file in os.listdir("latex/mock") if file.endswith(".asy")])+1):
        subprocess.run("asy --cd=latex/mock mock-{}.asy".format(i).split(" "))
    subprocess.run("pdflatex -interaction=nonstopmode -output-directory=latex/mock mock.tex".split(" "))
    await message.channel.send("Sending mock...")    
    await message.author.send("Here is your mock.", file=discord.File("latex/mock/mock.pdf"))
    await message.author.send("You will be dmed again in {} seconds with an answer key if applicable and links to solutions for each problem.".format(contests[contest]["time"]))
    await asyncio.sleep(contests[contest]["time"])
    answer_text=""
    if contests[contest]["answer"]:
        answer_text="Answers to mock\n"
        for i in range(len(problems)):
            answer_text+="{}: {}\n".format(i+1, problems[i].answer)
    links_text="Links to mock\n"
    for i in range(len(problems)):
        links_text+="{}: {} {}\n".format(i+1, problems[i].urls["forum"], problems[i].urls["wiki"])
    with open("latex/mock/links.txt", "w") as links_file:
        links_file.write(links_text)
        links_file.flush()
        return await message.author.send(answer_text, file=discord.File("latex/mock/links.txt"))

def format_latex(text):
    return remove_trailing(text.replace("defaultpen(white)","defaultpen(black)"))

def remove_trailing(text):
    if text.endswith("\\") or text.endswith("\n") or text.endswith("\r"):
        return remove_trailing(text[:-2])
    else:
        return text
