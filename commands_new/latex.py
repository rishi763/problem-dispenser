import discord
import subprocess
import os

def latex(args, author):  
    args=" ".join(args)
    path="latex/{}".format(author.id)
    try: 
        os.mkdir(path)
    except OSError:
        pass

    latex_writer=open("{}/statement.tex".format(path), "w")
    latex_writer.write("\\documentclass[preview, border=5pt]{{standalone}}\n\\usepackage{{amsmath}}\n\\usepackage{{amsfonts}}\n\\usepackage{{amssymb}}\n\\usepackage{{asymptote}}\n\\usepackage{{xcolor}}\n\\definecolor{{discord}}{{HTML}}{{36393E}}\n\\begin{{document}}\n\\color{{white}}\n\\pagecolor{{discord}}\n{}\n\\end{{document}}".format(args))
    latex_writer.close()
    process=None
    try:
        subprocess.run("pdflatex -interaction=nonstopmode -output-directory={} statement.tex".format(path).split(" "), timeout=10)
    except Exception as e:
        print(e)
        return [{"text":"Your LaTeX failed to compile properly."}]
    subprocess.run("gs -sDEVICE=png16m -dTextAlphaBits=4 -r600 -o {0}/statement.png {0}/statement.pdf".format(path).split(" "))
    # process=asyncio.create_subprocess_shell("cd {path} & pdflatex statement.tex & gswin64c -sDEVICE=png16m -dTextAlphaBits=4 -r600 -o statement.png statement.pdf".format(path=path))
    # try:
    #     await asyncio.wait_for(process, 10)
    #     return await message.channel.send(file=discord.File("{}/statement.png".format(path)))
    # except asyncio.CancelledError:
    #     process.terminate()
    return [{"file":"{}/statement.png".format(path)}]
    

