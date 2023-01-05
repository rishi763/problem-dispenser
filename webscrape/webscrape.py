from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
#from classifier import classify
import time
import os
import json

browser=asymptote=failed=None


update=False
metadata=True
compile=True

ahsme=open("webscrape/ahsme.txt", "r")

def main():
    global browser,asymptote,failed
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--enable-javascript")
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    asymptote = open("webscrape/asy.txt", "a")
    failed = open("webscrape/failed.txt", "a")


def to_latex(problem_statement):
    images = problem_statement.find_elements(By.TAG_NAME, "img")
    latex_text = problem_statement.get_attribute("innerHTML")
    for image in images:
        latex_text = latex_text.replace(image.get_attribute(
            "outerHTML"), image.get_attribute("alt"))
    latex_text = latex_text.replace("<span style=\"white-space:pre;\">", "").replace("<span style=\"white-space:nowrap;\">", "").replace("</span>", "\
").replace("<ul class=\"bbcode_list\">", "\\begin{itemize}").replace("</ul>", "\\end{itemize}").replace("<ol class=\"bbcode_list\" style=\"list-\
style-type:lower-alpha\">", "\\begin{enumerate}").replace("<ol class=\"bbcode_list\">", "\\begin{enumerate}").replace("</ol>", "\\end{enumerate}").replace("#", "\\#").replace("<li>", "\\item ").replace("</li>", "\
").replace("<br>", "\\\\").replace("<i>", "\\textit{").replace("</i>", "}").replace("<b>", "\\textbf{").replace("</b>", "}").replace("\\en\
d{itemize}\n\\\\", "\\end{itemize}").replace("\\end{enumerate}\n\\\\", "\\end{enumerate}").replace("\\begin{itemize}\\\\", "\\begin{item\
ize}").replace("\\end{itemize}\\\\", "\\end{itemize}").replace("\\begin{enumerate}\\\\", "\\begin{enumerate}").replace("\\end{enumerate}\\\\",
"\\end{enumerate}").replace("\\overarc", "\\overset{\\frown}").replace('’', "'").replace('“', '"').replace('”', '"').replace("—", "-").replace("ﬁ", "fi").replace("ﬀ", "ff").replace("\
–", "-").replace("ﬂ", "fl").replace("•", "$\\bullet$").replace("…", "\\dots").replace("¢", " cents").replace("é", "e").replace("·", "").replace("&lt;","<").replace("&gt;",">").replace("<div class=\"bbcode_center\" style=\"text-align:center\">","\\begin{center}").replace("</div>","\\end{center}\n")
    if "[asy]" in latex_text:
        latex_text = latex_text.replace("[asy]", "\n\\begin{asy}\nimport olympiad;\nimport cse5;\ndefaultpen(white);\nsize(100);\n").replace(
            "[/asy]", "\n\\end{asy}\n\\\\\n")
        return latex_text, True
    return latex_text, False


def get_html(url, skips=[]):
    browser.get(url)
    elements = browser.find_elements(By.CLASS_NAME, "cmty-view-posts-item")
    while(len(elements)==0):
        elements = browser.find_elements(By.CLASS_NAME, "cmty-view-posts-item")
    problems = []
    version = -1
    for item in elements:
        if len(item.find_elements(By.CLASS_NAME, "cmty-view-post-item-label")) == 0:
            for skip in skips:
                if skip in item.find_element(By.CLASS_NAME, "cmty-view-post-item-text").get_attribute("innerHTML").lower():
                    break
            else:
                version += 1
                problems.append([item.find_element(
                    By.CLASS_NAME, "cmty-view-post-item-text").get_attribute("innerHTML")])
        else:
            try:
                int(item.find_element(By.CLASS_NAME, "cmty-view-post-item-label").get_attribute("innerHTML"))
                if problems == []:
                     version = 0
                     problems.append([""])
                url=item.find_element(By.CLASS_NAME,"cmty-view-post-poster").find_element(By.CLASS_NAME,"cmty-view-post-topic-link").find_element(By.TAG_NAME,"a").get_attribute("href")
                latex, asy=to_latex(item.find_element(By.CLASS_NAME, "cmty-view-post-item-text"))
                problems[version].append({"latex":latex,"asy":asy,"url":url})
            except ValueError as e:
                version=version
    return problems


def get_urls(contest_url):
    urls = []
    browser.get(contest_url)
    time.sleep(10)
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        new_height = browser.execute_script(
            "return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    pages = browser.find_elements(By.CLASS_NAME, "cmty-category-cell-folder")
    for page in pages:
        urls.append(page.find_element(By.TAG_NAME, "a").get_attribute("href"))
    return urls[::-1]

def write_logs(path, latex_text):
    asymptote.write(path+"\n")
    failed.write(path+'\n')
    asymptote.write(latex_text+'\n\n')
    failed.flush()
    asymptote.flush()

def compile(latex_text, asy, path):
    fout = open("webscrape/latex/statement.tex", "w", encoding="utf-8")
    fout.write("\\documentclass[preview, border=5pt]{standalone}\n\\usepackage{amsmath}\n\\usepackage{amsfonts}\n\\usepackage{amssymb}\n\\usepackage{asymptote}\n\\usepackage{xcolor}\n\\definecolor{discord}{HTML}{36393E}\n\\begin{document}\n\\color{white}\n\\pagecolor{discord}\n"+latex_text+"\n\\end{document}")
    fout.close()
    #Current asymptote bug fails for these problems
    if path in ["2008/AMC/10A/21", "2015/AMC/10B/17", "2005/AMC/12A/17", "2012/AMC/12B/19", "2002/AMC/12A/25", "1983/AIME/11", "2015/AIME/I/15","2013/AMC/8/2","2013/AMC/8/4","2013/AMC/8/18","2015/AMC/8/12","2015/AMC/8/20"]:
        write_logs(path,latex_text)    
        return 0
    if asy:
        os.system("cd webscrape/latex & pdflatex -interaction=nonstopmode statement.tex")
        for i in range(1,len([file for file in os.listdir("webscrape/latex") if file.endswith(".asy")])+1):
            os.system("asy --cd=webscrape/latex statement-{}.asy".format(i))
        os.system("cd webscrape/latex & pdflatex -interaction=nonstopmode statement.tex & gswin64c -sDEVICE=png16m -dTextAlphaBits=4 -r600 -o statement.png statement.pdf")
        write_logs(path,latex_text)
        if update:
            try:
                os.replace(
                    "webscrape/latex/statement.png", "data/problems/{}/statement.png".format(path))
            except:
                print("Failed to update files.")
                os.replace("webscrape/latex/statement.png", "webscrape/data/{}/statement.png".format(path))
        else:
            os.replace("webscrape/latex/statement.png", "webscrape/data/{}/statement.png".format(path))
    else:
        os.system("cd webscrape/latex & pdflatex -interaction=nonstopmode statement.tex & gswin64c -sDEVICE=png16m -dTextAlphaBits=4 -r600 -o statement.png statement.pdf")
        if update:
            try:
                os.replace("webscrape/latex/statement.png", "data/problems/{}/statement.png".format(path))
            except:
                print("Failed to update files.")
        else:
            os.replace("webscrape/latex/statement.png", "webscrape/data/{}/statement.png".format(path))

def get_answer(path):
    return ahsme.readline().replace("\n","")
    try:
        answer_path="data/problems/{}/info.json".format(path)
        with open(answer_path,"r") as answer_read:
            data=json.load(answer_read)
            return data["answer"]
    except Exception as e:
        print(e)
        return None



def set_metadata(path, answer=None, latex=None, url=None):
    info_path=""
    if update:
        info_path="data/problems/{}/info.json".format(path)
    else:
        info_path="webscrape/data/{}/info.json".format(path)
    data={}
    if answer is not None:
        data["answer"]=answer
    if latex is not None:
        data["latex"]=latex
    if url is not None:
        data["url"]=url
    #data["category"]=classify.classify(path)
    with open(info_path, 'w') as data_file:
        json.dump(data, data_file)

def get_problems(urls):
    contests={
        "aime_problems":["AIME/", ["mar", "jun", "apr", "feb"], ["II", "I"]],
        "amc_8":["AMC/8", [], []],
        "amc_10":["AMC/10", ["feb"], ["A", "B", "P"]],
        "amc_12ahsme":["AMC/12", ["feb", "dec"], ["A", "B", "P"]],
        "amc_12ahsme1":["AHSME/", [], []],
        "harvardmit_mathematics_tournament":["HMMT/", ["feb"], [["NOV", "GEN"], ["NOV", "GUTS"], ["NOV", "TEAM"], ["NOV", "THEME"], "ALG", "GEO", "COM", "TEAM", "CALC", "ADV", "GUTS", "GEN", "ORAL"]],
        "imo":["IMO/",["day"] ,[]],
        "usajmo":["USAJMO/",["day"] ,[]],
        "usamo":["USAMO/", ["day"], []],
        "usojmo":["USAJMO/",["day"] ,[]],
        "usomo":["USAMO/", ["day"], []]
    }
    if update:
        base_path="data/problems"
    else:
        base_path="webscrape/data"
    for url in urls:
        year = url.split("_")[1]
        if year[0]=="1" and "amc_12ahsme" in url:
            url=url.replace("amc_12ahsme", "amc_12ahsme1")
        [name, skips, categories]=contests["_".join(url.replace("_spring", "").split("_")[2:])]
        try:
            os.mkdir("{}/{}".format(base_path, year))
        except OSError as e:
            print(e)
        try:
            os.mkdir("{}/{}/{}".format(base_path, year,name.split('/')[0]))
        except OSError as e:
            print(e)     
        problems = get_html(url, skips)
        for row in problems:
            if len(row)==0:
                continue
            for category in categories:
                if isinstance(category, list):
                    for word in category:
                        if word not in row[0].upper():
                            break
                    else:
                        path="{}/{}{}/".format(year,name,"".join(category))
                        break
                else:
                    if category in row[0].upper():
                        path="{}/{}{}/".format(year,name,category)
                        break
            else:
                path="{}/{}".format(year,name)
                path+='/'*(1-path.endswith('/'))
            if problems.index(row)!=len(problems)-1:
                try:
                    os.mkdir("{}/{}".format(base_path, path))
                except OSError as e:
                    print(e)
            for i in range(len(row)):
                if i>0:
                    problem=row[i]
                    try:
                        os.mkdir("{}/{}{}".format(base_path, path, i))
                    except OSError as e:
                        print(e)
                    if metadata:
                        set_metadata(path+str(i), answer=get_answer(path+str(i)), latex=problem["latex"], url=problem["url"], )
                    if compile:
                        compile(problem["latex"], problem["asy"], path+str(i))

AIME=["https://artofproblemsolving.com/community/c4880_1983_aime_problems", "https://artofproblemsolving.com/community/c4881_1984_aime_problems", "https://artofproblemsolving.com/community/c4882_1985_aime_problems", "https://artofproblemsolving.com/community/c4883_1986_aime_problems", "https://artofproblemsolving.com/community/c4884_1987_aime_problems", "https://artofproblemsolving.com/community/c4885_1988_aime_problems", "https://artofproblemsolving.com/community/c4886_1989_aime_problems", "https://artofproblemsolving.com/community/c4887_1990_aime_problems", "https://artofproblemsolving.com/community/c4888_1991_aime_problems", "https://artofproblemsolving.com/community/c4889_1992_aime_problems", "https://artofproblemsolving.com/community/c4890_1993_aime_problems", "https://artofproblemsolving.com/community/c4891_1994_aime_problems", "https://artofproblemsolving.com/community/c4892_1995_aime_problems", "https://artofproblemsolving.com/community/c4893_1996_aime_problems", "https://artofproblemsolving.com/community/c4894_1997_aime_problems", "https://artofproblemsolving.com/community/c4895_1998_aime_problems", "https://artofproblemsolving.com/community/c4896_1999_aime_problems", "https://artofproblemsolving.com/community/c4897_2000_aime_problems", "https://artofproblemsolving.com/community/c4898_2001_aime_problems", "https://artofproblemsolving.com/community/c4899_2002_aime_problems", "https://artofproblemsolving.com/community/c4900_2003_aime_problems", "https://artofproblemsolving.com/community/c4901_2004_aime_problems", "https://artofproblemsolving.com/community/c4902_2005_aime_problems", "https://artofproblemsolving.com/community/c4903_2006_aime_problems", "https://artofproblemsolving.com/community/c4904_2007_aime_problems", "https://artofproblemsolving.com/community/c4905_2008_aime_problems", "https://artofproblemsolving.com/community/c4906_2009_aime_problems", "https://artofproblemsolving.com/community/c4907_2010_aime_problems", "https://artofproblemsolving.com/community/c4908_2011_aime_problems", "https://artofproblemsolving.com/community/c4909_2012_aime_problems", "https://artofproblemsolving.com/community/c4910_2013_aime_problems", "https://artofproblemsolving.com/community/c4911_2014_aime_problems", "https://artofproblemsolving.com/community/c47708_2015_aime_problems", "https://artofproblemsolving.com/community/c240633_2016_aime_problems", "https://artofproblemsolving.com/community/c421306_2017_aime_problems", "https://artofproblemsolving.com/community/c588208_2018_aime_problems", "https://artofproblemsolving.com/community/c847267_2019_aime_problems", "https://artofproblemsolving.com/community/c1117986_2020_aime_problems", "https://artofproblemsolving.com/community/c1970738_2021_aime_problems"]
AHSME=['https://artofproblemsolving.com/community/c4814_1950_amc_12ahsme', 'https://artofproblemsolving.com/community/c4815_1951_amc_12ahsme', 'https://artofproblemsolving.com/community/c4816_1952_amc_12ahsme', 'https://artofproblemsolving.com/community/c4817_1953_amc_12ahsme', 'https://artofproblemsolving.com/community/c4818_1954_amc_12ahsme', 'https://artofproblemsolving.com/community/c4819_1955_amc_12ahsme', 'https://artofproblemsolving.com/community/c4820_1956_amc_12ahsme', 'https://artofproblemsolving.com/community/c4821_1957_amc_12ahsme', 'https://artofproblemsolving.com/community/c4822_1958_amc_12ahsme', 'https://artofproblemsolving.com/community/c4823_1959_amc_12ahsme', 'https://artofproblemsolving.com/community/c4824_1960_amc_12ahsme', 'https://artofproblemsolving.com/community/c4825_1961_amc_12ahsme', 'https://artofproblemsolving.com/community/c4826_1962_amc_12ahsme', 'https://artofproblemsolving.com/community/c4827_1963_amc_12ahsme', 'https://artofproblemsolving.com/community/c4828_1964_amc_12ahsme', 'https://artofproblemsolving.com/community/c4829_1965_amc_12ahsme', 'https://artofproblemsolving.com/community/c4830_1966_amc_12ahsme', 'https://artofproblemsolving.com/community/c4831_1967_amc_12ahsme', 'https://artofproblemsolving.com/community/c4832_1968_amc_12ahsme', 'https://artofproblemsolving.com/community/c4833_1969_amc_12ahsme', 'https://artofproblemsolving.com/community/c4834_1970_amc_12ahsme', 'https://artofproblemsolving.com/community/c4835_1971_amc_12ahsme', 'https://artofproblemsolving.com/community/c4836_1972_amc_12ahsme', 'https://artofproblemsolving.com/community/c4837_1973_amc_12ahsme', 'https://artofproblemsolving.com/community/c4838_1974_amc_12ahsme', 'https://artofproblemsolving.com/community/c4839_1975_amc_12ahsme', 'https://artofproblemsolving.com/community/c4840_1976_amc_12ahsme', 'https://artofproblemsolving.com/community/c4841_1977_amc_12ahsme', 'https://artofproblemsolving.com/community/c4842_1978_amc_12ahsme', 'https://artofproblemsolving.com/community/c4843_1979_amc_12ahsme', 'https://artofproblemsolving.com/community/c4844_1980_amc_12ahsme', 'https://artofproblemsolving.com/community/c4845_1981_amc_12ahsme', 'https://artofproblemsolving.com/community/c4846_1982_amc_12ahsme', 'https://artofproblemsolving.com/community/c4847_1983_amc_12ahsme', 'https://artofproblemsolving.com/community/c4848_1984_amc_12ahsme', 'https://artofproblemsolving.com/community/c4849_1985_amc_12ahsme', 'https://artofproblemsolving.com/community/c4850_1986_amc_12ahsme', 'https://artofproblemsolving.com/community/c4851_1987_amc_12ahsme', 'https://artofproblemsolving.com/community/c4852_1988_amc_12ahsme', 'https://artofproblemsolving.com/community/c4853_1989_amc_12ahsme', 'https://artofproblemsolving.com/community/c4854_1990_amc_12ahsme', 'https://artofproblemsolving.com/community/c4855_1991_amc_12ahsme', 'https://artofproblemsolving.com/community/c4856_1992_amc_12ahsme', 'https://artofproblemsolving.com/community/c4857_1993_amc_12ahsme', 'https://artofproblemsolving.com/community/c4858_1994_amc_12ahsme', 'https://artofproblemsolving.com/community/c4859_1995_amc_12ahsme', 'https://artofproblemsolving.com/community/c4860_1996_amc_12ahsme', 'https://artofproblemsolving.com/community/c4861_1997_amc_12ahsme', 'https://artofproblemsolving.com/community/c4862_1998_amc_12ahsme', 'https://artofproblemsolving.com/community/c4863_1999_amc_12ahsme']
AMC8=['https://artofproblemsolving.com/community/c4782_1999_amc_8', 'https://artofproblemsolving.com/community/c4783_2000_amc_8', 'https://artofproblemsolving.com/community/c4784_2001_amc_8', 'https://artofproblemsolving.com/community/c4785_2002_amc_8', 'https://artofproblemsolving.com/community/c4786_2003_amc_8', 'https://artofproblemsolving.com/community/c4787_2004_amc_8', 'https://artofproblemsolving.com/community/c4788_2005_amc_8', 'https://artofproblemsolving.com/community/c4789_2006_amc_8', 'https://artofproblemsolving.com/community/c4790_2007_amc_8', 'https://artofproblemsolving.com/community/c4791_2008_amc_8', 'https://artofproblemsolving.com/community/c4792_2009_amc_8', 'https://artofproblemsolving.com/community/c4793_2010_amc_8', 'https://artofproblemsolving.com/community/c4794_2011_amc_8', 'https://artofproblemsolving.com/community/c4795_2012_amc_8', 'https://artofproblemsolving.com/community/c4796_2013_amc_8', 'https://artofproblemsolving.com/community/c4797_2014_amc_8', 'https://artofproblemsolving.com/community/c185369_2015_amc_8', 'https://artofproblemsolving.com/community/c374738_2016_amc_8', 'https://artofproblemsolving.com/community/c588215_2017_amc_8', 'https://artofproblemsolving.com/community/c776909_2018_amc_8', 'https://artofproblemsolving.com/community/c1015559_2019_amc_8', 'https://artofproblemsolving.com/community/c1975275_2020_amc_8']
AMC10=["https://artofproblemsolving.com/community/c4798_2000_amc_10","https://artofproblemsolving.com/community/c4799_2001_amc_10","https://artofproblemsolving.com/community/c4800_2002_amc_10","https://artofproblemsolving.com/community/c4801_2003_amc_10","https://artofproblemsolving.com/community/c4802_2004_amc_10","https://artofproblemsolving.com/community/c4803_2005_amc_10","https://artofproblemsolving.com/community/c4804_2006_amc_10","https://artofproblemsolving.com/community/c4805_2007_amc_10","https://artofproblemsolving.com/community/c4806_2008_amc_10","https://artofproblemsolving.com/community/c4807_2009_amc_10","https://artofproblemsolving.com/community/c4808_2010_amc_10","https://artofproblemsolving.com/community/c4809_2011_amc_10","https://artofproblemsolving.com/community/c4810_2012_amc_10","https://artofproblemsolving.com/community/c4811_2013_amc_10","https://artofproblemsolving.com/community/c4812_2014_amc_10","https://artofproblemsolving.com/community/c4813_2015_amc_10","https://artofproblemsolving.com/community/c222490_2016_amc_10","https://artofproblemsolving.com/community/c408752_2017_amc_10","https://artofproblemsolving.com/community/c588207_2018_amc_10","https://artofproblemsolving.com/community/c448656_2019_amc_10","https://artofproblemsolving.com/community/c1116106_2020_amc_10", "https://artofproblemsolving.com/community/c1975144_2021_amc_10_spring"]
AMC12=["https://artofproblemsolving.com/community/c4864_2000_amc_12ahsme","https://artofproblemsolving.com/community/c4865_2001_amc_12ahsme","https://artofproblemsolving.com/community/c4866_2002_amc_12ahsme","https://artofproblemsolving.com/community/c4867_2003_amc_12ahsme","https://artofproblemsolving.com/community/c4868_2004_amc_12ahsme","https://artofproblemsolving.com/community/c4869_2005_amc_12ahsme","https://artofproblemsolving.com/community/c4870_2006_amc_12ahsme","https://artofproblemsolving.com/community/c4871_2007_amc_12ahsme","https://artofproblemsolving.com/community/c4872_2008_amc_12ahsme","https://artofproblemsolving.com/community/c4873_2009_amc_12ahsme","https://artofproblemsolving.com/community/c4874_2010_amc_12ahsme","https://artofproblemsolving.com/community/c4875_2011_amc_12ahsme","https://artofproblemsolving.com/community/c4876_2012_amc_12ahsme","https://artofproblemsolving.com/community/c4877_2013_amc_12ahsme","https://artofproblemsolving.com/community/c4878_2014_amc_12ahsme","https://artofproblemsolving.com/community/c4879_2015_amc_12ahsme","https://artofproblemsolving.com/community/c224119_2016_amc_12ahsme","https://artofproblemsolving.com/community/c406362_2017_amc_12ahsme","https://artofproblemsolving.com/community/c588206_2018_amc_12ahsme","https://artofproblemsolving.com/community/c826140_2019_amc_12ahsme","https://artofproblemsolving.com/community/c1116107_2020_amc_12ahsme", "https://artofproblemsolving.com/community/c1975145_2021_amc_12ahsme_spring"]
HMMT=["https://artofproblemsolving.com/community/c3619_1998_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c3620_1999_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c3621_2000_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c3622_2004_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c3623_2005_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c3624_2006_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c3625_2007_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c3626_2008_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c3627_2009_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c3628_2010_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c3629_2011_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c3630_2012_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c3631_2013_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c3632_2014_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c53934_2015_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c386695_2016_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c413396_2017_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c1254477_2018_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c832201_2019_harvardmit_mathematics_tournament","https://artofproblemsolving.com/community/c1074888_2020_harvardmit_mathematics_tournament"]
USAJMO=["https://artofproblemsolving.com/community/c3973_2010_usajmo","https://artofproblemsolving.com/community/c3974_2011_usajmo","https://artofproblemsolving.com/community/c3975_2012_usajmo","https://artofproblemsolving.com/community/c3976_2013_usajmo","https://artofproblemsolving.com/community/c3977_2014_usajmo","https://artofproblemsolving.com/community/c70922_2015_usajmo","https://artofproblemsolving.com/community/c259907_2016_usajmo","https://artofproblemsolving.com/community/c439885_2017_usajmo","https://artofproblemsolving.com/community/c615274_2018_usajmo","https://artofproblemsolving.com/community/c862373_2019_usajmo","https://artofproblemsolving.com/community/c1209090_2020_usojmo"]
USAMO=["https://artofproblemsolving.com/community/c4470_1972_usamo","https://artofproblemsolving.com/community/c4471_1973_usamo","https://artofproblemsolving.com/community/c4472_1974_usamo","https://artofproblemsolving.com/community/c4473_1975_usamo","https://artofproblemsolving.com/community/c4474_1976_usamo","https://artofproblemsolving.com/community/c4475_1977_usamo","https://artofproblemsolving.com/community/c4476_1978_usamo","https://artofproblemsolving.com/community/c4477_1979_usamo","https://artofproblemsolving.com/community/c4478_1980_usamo","https://artofproblemsolving.com/community/c4479_1981_usamo","https://artofproblemsolving.com/community/c4480_1982_usamo","https://artofproblemsolving.com/community/c4481_1983_usamo","https://artofproblemsolving.com/community/c4482_1984_usamo","https://artofproblemsolving.com/community/c4483_1985_usamo","https://artofproblemsolving.com/community/c4484_1986_usamo","https://artofproblemsolving.com/community/c4485_1987_usamo","https://artofproblemsolving.com/community/c4486_1988_usamo","https://artofproblemsolving.com/community/c4487_1989_usamo","https://artofproblemsolving.com/community/c4488_1990_usamo","https://artofproblemsolving.com/community/c4489_1991_usamo","https://artofproblemsolving.com/community/c4490_1992_usamo","https://artofproblemsolving.com/community/c4491_1993_usamo","https://artofproblemsolving.com/community/c4492_1994_usamo","https://artofproblemsolving.com/community/c4493_1995_usamo","https://artofproblemsolving.com/community/c4494_1996_usamo","https://artofproblemsolving.com/community/c4495_1997_usamo","https://artofproblemsolving.com/community/c4496_1998_usamo","https://artofproblemsolving.com/community/c4497_1999_usamo","https://artofproblemsolving.com/community/c4498_2000_usamo","https://artofproblemsolving.com/community/c4499_2001_usamo","https://artofproblemsolving.com/community/c4500_2002_usamo","https://artofproblemsolving.com/community/c4501_2003_usamo","https://artofproblemsolving.com/community/c4502_2004_usamo","https://artofproblemsolving.com/community/c4503_2005_usamo","https://artofproblemsolving.com/community/c4504_2006_usamo","https://artofproblemsolving.com/community/c4505_2007_usamo","https://artofproblemsolving.com/community/c4506_2008_usamo","https://artofproblemsolving.com/community/c4507_2009_usamo","https://artofproblemsolving.com/community/c4508_2010_usamo","https://artofproblemsolving.com/community/c4509_2011_usamo","https://artofproblemsolving.com/community/c4510_2012_usamo","https://artofproblemsolving.com/community/c4511_2013_usamo","https://artofproblemsolving.com/community/c4512_2014_usamo","https://artofproblemsolving.com/community/c70921_2015_usamo","https://artofproblemsolving.com/community/c259909_2016_usamo","https://artofproblemsolving.com/community/c439884_2017_usamo","https://artofproblemsolving.com/community/c644976_2018_usamo","https://artofproblemsolving.com/community/c862378_2019_usamo","https://artofproblemsolving.com/community/c1209089_2020_usomo"]
IMO=['https://artofproblemsolving.com/community/c3786_1959_imo', 'https://artofproblemsolving.com/community/c3787_1960_imo', 'https://artofproblemsolving.com/community/c3788_1961_imo', 'https://artofproblemsolving.com/community/c3789_1962_imo', 'https://artofproblemsolving.com/community/c3790_1963_imo', 'https://artofproblemsolving.com/community/c3791_1964_imo', 'https://artofproblemsolving.com/community/c3792_1965_imo', 'https://artofproblemsolving.com/community/c3793_1966_imo', 'https://artofproblemsolving.com/community/c3794_1967_imo', 'https://artofproblemsolving.com/community/c3795_1968_imo', 'https://artofproblemsolving.com/community/c3796_1969_imo', 'https://artofproblemsolving.com/community/c3797_1970_imo', 'https://artofproblemsolving.com/community/c3798_1971_imo', 'https://artofproblemsolving.com/community/c3799_1972_imo', 'https://artofproblemsolving.com/community/c3800_1973_imo', 'https://artofproblemsolving.com/community/c3801_1974_imo', 'https://artofproblemsolving.com/community/c3802_1975_imo', 'https://artofproblemsolving.com/community/c3803_1976_imo', 'https://artofproblemsolving.com/community/c3804_1977_imo', 'https://artofproblemsolving.com/community/c3805_1978_imo', 'https://artofproblemsolving.com/community/c3806_1979_imo', 'https://artofproblemsolving.com/community/c3807_1980_imo', 'https://artofproblemsolving.com/community/c3808_1981_imo', 'https://artofproblemsolving.com/community/c3809_1982_imo', 'https://artofproblemsolving.com/community/c3810_1983_imo', 'https://artofproblemsolving.com/community/c3811_1984_imo', 'https://artofproblemsolving.com/community/c3812_1985_imo', 'https://artofproblemsolving.com/community/c3813_1986_imo', 'https://artofproblemsolving.com/community/c3814_1987_imo', 'https://artofproblemsolving.com/community/c3815_1988_imo', 'https://artofproblemsolving.com/community/c3816_1989_imo', 'https://artofproblemsolving.com/community/c3817_1990_imo', 'https://artofproblemsolving.com/community/c3818_1991_imo', 'https://artofproblemsolving.com/community/c3819_1992_imo', 'https://artofproblemsolving.com/community/c3820_1993_imo', 'https://artofproblemsolving.com/community/c3821_1994_imo', 'https://artofproblemsolving.com/community/c3822_1995_imo', 'https://artofproblemsolving.com/community/c3823_1996_imo', 'https://artofproblemsolving.com/community/c3824_1997_imo', 'https://artofproblemsolving.com/community/c3825_1998_imo', 'https://artofproblemsolving.com/community/c3826_1999_imo', 'https://artofproblemsolving.com/community/c3827_2000_imo', 'https://artofproblemsolving.com/community/c3828_2001_imo', 'https://artofproblemsolving.com/community/c3829_2002_imo', 'https://artofproblemsolving.com/community/c3830_2003_imo', 'https://artofproblemsolving.com/community/c3831_2004_imo', 'https://artofproblemsolving.com/community/c3832_2005_imo', 'https://artofproblemsolving.com/community/c3833_2006_imo', 'https://artofproblemsolving.com/community/c3834_2007_imo', 'https://artofproblemsolving.com/community/c3835_2008_imo', 'https://artofproblemsolving.com/community/c3836_2009_imo', 'https://artofproblemsolving.com/community/c3837_2010_imo', 'https://artofproblemsolving.com/community/c3838_2011_imo', 'https://artofproblemsolving.com/community/c3839_2012_imo', 'https://artofproblemsolving.com/community/c3840_2013_imo', 'https://artofproblemsolving.com/community/c3841_2014_imo', 'https://artofproblemsolving.com/community/c105780_2015_imo', 'https://artofproblemsolving.com/community/c294448_2016_imo', 'https://artofproblemsolving.com/community/c481799_2017_imo', 'https://artofproblemsolving.com/community/c681585_2018_imo', 'https://artofproblemsolving.com/community/c912139_2019_imo', 'https://artofproblemsolving.com/community/c1306546_2020_imo']
main()


get_problems([AMC12[0]])
browser.quit() 
# smc=open("webscrape/smc.txt","r")
# smc_latex=smc.read().split("====\n")
# for i in range(1,26):
#     set_metadata("2020/SMC/{}".format(i), get_answer("2020/SMC/{}".format(i)), smc_latex[i-1], None)
# calt=open("webscrape/calt.txt","r")
# calt_latex=calt.read().split("====\n")
# for i in range(20):
#     set_metadata("2020/CALT/SPR/{}".format(i+1), get_answer("2020/CALT/SPR/{}".format(i+1)), calt_latex[i], None)
# for i in range(30):
#     set_metadata("2020/CALT/COUNT/{}".format(i+1), get_answer("2020/CALT/COUNT/{}".format(i+1)), calt_latex[i+20], None)
# for i in range(4):
#     set_metadata("2020/CALT/TAR/{}".format(i+1), get_answer("2020/CALT/TAR/{}".format(i+1)), calt_latex[i+50], None)
#get_problems(AHSME[:7]+AHSME[8:24]+AHSME[25:])

# for i in range(1,51):
#     path="data/problems/1957/AHSME/{}/info.json".format(i)
#     with open(path, "r") as json_file:
#         info=json.load(json_file)
#         with open(path, "w") as update_file:
#             data=info
#             data["answer"]="BEECBAEABCECCDBDABAAEACBBEABDDBEECDDCDEDDCBEAEAACB"[i-1]
#             json.dump(data,update_file)
