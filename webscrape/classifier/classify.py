from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os,sys
sys.path.append(os.getcwd())
from problem.problem import Problem

browser=None
ALG=["https://artofproblemsolving.com/wiki/index.php/Category:Introductory_Algebra_Problems", "https://artofproblemsolving.com/wiki/index.php?title=Category:Introductory_Algebra_Problems&pagefrom=1964+AHSME+Problems%2FProblem+15#mw-pages", "https://artofproblemsolving.com/wiki/index.php?title=Category:Introductory_Algebra_Problems&pagefrom=1986+AJHSME+Problems%2FProblem+7#mw-pages", "https://artofproblemsolving.com/wiki/index.php?title=Category:Introductory_Algebra_Problems&pagefrom=2000+AMC+10+Problems%2FProblem+20#mw-pages", "https://artofproblemsolving.com/wiki/index.php?title=Category:Introductory_Algebra_Problems&pagefrom=2007+Cyprus+MO%2FLyceum%2FProblem+8#mw-pages", "https://artofproblemsolving.com/wiki/index.php/Category:Intermediate_Algebra_Problems", "https://artofproblemsolving.com/wiki/index.php?title=Category:Intermediate_Algebra_Problems&pagefrom=2000+AIME+II+Problems%2FProblem+13#mw-pages", "https://artofproblemsolving.com/wiki/index.php?title=Category:Intermediate_Algebra_Problems&pagefrom=2017+AMC+12B+Problems%2FProblem+20#mw-pages", "https://artofproblemsolving.com/wiki/index.php/Category:Olympiad_Algebra_Problems"]
COM=["https://artofproblemsolving.com/wiki/index.php/Category:Introductory_Combinatorics_Problems", "https://artofproblemsolving.com/wiki/index.php/Category:Intermediate_Combinatorics_Problems", "https://artofproblemsolving.com/wiki/index.php?title=Category:Intermediate_Combinatorics_Problems&pagefrom=2018+UNM-PNM+Statewide+High+School+Mathematics+Contest+II+Problems%2FProblem+8#mw-pages", "https://artofproblemsolving.com/wiki/index.php/Category:Olympiad_Combinatorics_Problems", "https://artofproblemsolving.com/wiki/index.php/Category:Introductory_Probability_Problems", "https://artofproblemsolving.com/wiki/index.php/Category:Intermediate_Probability_Problems"]
GEO=["https://artofproblemsolving.com/wiki/index.php/Category:Introductory_Geometry_Problems", "https://artofproblemsolving.com/wiki/index.php?title=Category:Introductory_Geometry_Problems&pagefrom=1995+AHSME+Problems%2FProblem+18#mw-pages", "https://artofproblemsolving.com/wiki/index.php?title=Category:Introductory_Geometry_Problems&pagefrom=2009+AMC+12B+Problems%2FProblem+14#mw-pages", "https://artofproblemsolving.com/wiki/index.php/Category:Intermediate_Geometry_Problems", "https://artofproblemsolving.com/wiki/index.php?title=Category:Intermediate_Geometry_Problems&pagefrom=2002+Pan+African+MO+Problems%2FProblem+2#mw-pages", "https://artofproblemsolving.com/wiki/index.php?title=Category:Intermediate_Geometry_Problems&pagefrom=2020+AIME+II+Problems%2FProblem+4#mw-pages", "https://artofproblemsolving.com/wiki/index.php/Category:Olympiad_Geometry_Problems", "https://artofproblemsolving.com/wiki/index.php/Category:Introductory_Trigonometry_Problems", "https://artofproblemsolving.com/wiki/index.php/Category:Intermediate_Trigonometry_Problems", "https://artofproblemsolving.com/wiki/index.php/Category:Olympiad_Trigonometry_Problems"]
NUM=["https://artofproblemsolving.com/wiki/index.php/Category:Introductory_Number_Theory_Problems", "https://artofproblemsolving.com/wiki/index.php/Category:Intermediate_Number_Theory_Problems", "https://artofproblemsolving.com/wiki/index.php?title=Category:Intermediate_Number_Theory_Problems&pagefrom=2017+AIME+I+Problems%2FProblem+14#mw-pages", "https://artofproblemsolving.com/wiki/index.php/Category:Olympiad_Number_Theory_Problems"]
ALG_LINKS=[]
COM_LINKS=[]
GEO_LINKS=[]
NUM_LINKS=[]


def main():
    global browser
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--enable-javascript")
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

def scrape_url(url):
    browser.get(url)
    try:
        problems=browser.find_element(By.CLASS_NAME, "mw-category").find_elements(By.TAG_NAME, "a")
    except Exception as e:
        print("Expected error")
        problems=browser.find_element(By.CLASS_NAME, "mw-category-generated").find_elements(By.TAG_NAME, "a")
    return [problem.get_attribute("href")for problem in problems]


def get_problems():
    global ALG_LINKS, COM_LINKS,  GEO_LINKS, NUM_LINKS
    for source in ALG:
        ALG_LINKS+=scrape_url(source)
    for source in COM:
        COM_LINKS+=scrape_url(source)
    for source in GEO:
        GEO_LINKS+=scrape_url(source)
    for source in NUM:
        NUM_LINKS+=scrape_url(source)

def get_problem_from_path(path):
    if path.count("/")==2:
        year, contest, number=path.split("/")
        version="None"
    elif "AMC" in path: 
        year, a, b, number=path.split("/")
        if "AMC/8" in path or not ("A" in b or "B" in b or "P" in b):
            contest=a+"/"+b
            version="None"
        else:
            contest=(a+"/"+b)[:-1]
            version=(a+b)[-1]
    else:
        year, contest, version, number=path.split("/")
    return Problem(dict={"year": year, "contest": contest, "number": number, "version": version})

def classify(path):
    url=get_problem_from_path(path).urls["wiki"]
    if url in ALG_LINKS:
        return "A"
    if url in COM_LINKS:
        return "C"
    if url in GEO_LINKS:
        return "G"
    if url in NUM_LINKS:
        return "N"
    return ""

main()
get_problems()
browser.quit()
