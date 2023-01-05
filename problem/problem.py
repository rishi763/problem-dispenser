import random
import json
import time
import sys

contests=None
difficulties={
    "insane":"insane",
    "hard":"hard",
    "middle":"medium",
    "medium":"medium",
    "med":"medium",
    "easy":"easy",
    "ez":"easy"
}
def main():
    sys.setrecursionlimit(100)
    global contests
    with open("problem/contests.json", "r") as contests_file:
        contests=json.load(contests_file)
    

class Problem:
    def __init__(self, args=None, dict=None):
        if dict is None:
            self.parse(args)
            self.start_time=time.time()
        else:
            self.__dict__=dict
            self.make_path()
            self.get_data()
    
    def __str__(self):
        str="Source: {self.path}\n".format(self=self)
        if self.answer is not None:
            str+="Answer: ||{self.answer}||\n".format(self=self)
        if self.urls["forum"] is not None:
            str+="Forum Link: {self.urls[forum]}\n".format(self=self)
        if self.urls["forum"] is not None:
            str+="Wiki Link: {self.urls[wiki]}\n".format(self=self)
        return str

    def parse(self, args):
        self.year=None
        self.contest=None
        self.version=None
        self.number=None
        self.category=None
        chosen=False
        new="new" in args
        
        for key in contests:
            to_break=False
            for alias in contests[key]["aliases"]:
                if alias.lower() in args:
                    self.valid=True
                    self.contest=key
                    to_break=True
                    break
            if to_break:
                break
        else:
            self.valid=False
            return None
        contest_data=contests[self.contest]
        self.attempts=contest_data["attempts"]

        if contest_data["choice"]:
            for version in contest_data["versions"]:
                to_break=False
                for alias in contest_data[version]["aliases"]:
                    if alias.lower() in args:
                        self.version=version
                        chosen=True
                        to_break=True
                        break
                if to_break:
                    break
            else:
                if new:
                    self.version=random.choices(population=[version for version in contest_data["versions"] if contest_data[version]["new"]], weights=[contest_data[version]["weight"] for version in contest_data["versions"] if contest_data[version]["new"]])[0]
                else:
                    self.version=random.choices(population=contest_data["versions"], weights=[contest_data[version]["weight"] for version in contest_data["versions"]])[0]
                
        else:
            if new:
                self.version=random.choices(population=[version for version in contest_data["versions"] if contest_data[version]["new"]], weights=[contest_data[version]["weight"] for version in contest_data["versions"] if contest_data[version]["new"]])[0]
            else:
         
                self.version=random.choices(population=contest_data["versions"], weights=[contest_data[version]["weight"] for version in contest_data["versions"]])[0]
        if new and not chosen:
            self.year=random.choice([year for year in contest_data[self.version]["years"] if year>=2010])
        else:
            self.year=random.choice(contest_data[self.version]["years"])

        for key in difficulties:
            if key in args:
                self.difficulty=difficulties[key]
                self.number=random.choice(contest_data[self.version][self.difficulty])
                break
        else:
            self.difficulty=random.choice(["easy","medium","hard"])
            self.number=random.choice(contest_data[self.version][self.difficulty])

        self.make_path()
        self.get_data()

        if not self.valid:
            return None

        if "alg" in args and self.category!="A":
            self.parse(args)
        if "com" in args and self.category!="C":
            self.parse(args)
        if "geo" in args and self.category!="G":
            self.parse(args)
        if ("nt" in args or "num" in args) and self.category!="N":
            self.parse(args)

    def rating_updates(self):
        update_list={}
        contest_data=contests[self.contest]
        if contest_data["answer"]:
            if self.attempts==0:
                update_list[contest_data["rating_name"]+"_FAILED"]=1
                update_list["TOTAL_FAILED"]=1
            else:
                update_list[contest_data["rating_name"]+"_SOLVED"]=1
                update_list["TOTAL_SOLVED"]=1
        if contest_data["rated"]:
            if self.attempts>0:
                update_list[contest_data["rating_name"]+"_RATING"]=contest_data["difficulty_weight"][["easy", "medium", "hard", "insane"].index(self.difficulty)]*contest_data["attempt_weight"][self.attempts-1]/10
                update_list["TOTAL_RATING"]=update_list[contest_data["rating_name"]+"_RATING"]*contest_data["contest_weight"]/10
        return update_list


    def make_path(self):
        if self.version.startswith("None"):
            self.path="{}/{}/{}".format(self.year, self.contest, self.number)
        elif "/" in self.contest:
            self.path="{}/{}{}/{}".format(self.year, self.contest, self.version, self.number)
        else:
            self.path="{}/{}/{}/{}".format(self.year, self.contest, self.version, self.number)

            
    def get_data(self):
        
        self.urls={}
        contest_data=contests[self.contest]
        try:
            with open("data/problems/{}/info.json".format(self.path),"r") as file:
                data=json.load(file)
                if contest_data["answer"]:
                    self.answer=data["answer"]
                else:
                    self.answer=None
                
                self.urls["forum"]=data.get("url", None)
                self.latex=data["latex"]
                self.category=data["category"]
        except Exception as e:
            print(self.path)
            print(e)
            self.valid=False
        if contest_data["url"] is not None:
            if self.version.startswith("None"):
                self.urls["wiki"]=contest_data["url"].replace("YEAR", str(self.year)).replace("NUMBER", str(self.number)).replace("VERSION", "").replace("__","_")
            else:
                self.urls["wiki"]=contest_data["url"].replace("YEAR", str(self.year)).replace("NUMBER", str(self.number)).replace("VERSION", self.version)
        else:
            self.urls["wiki"]=None
    def get_image(self):
        try:
            return "data/problems/{}/statement.png".format(self.path)
        except:
            print("Problem ", self.path, " not found")
            self.valid=False
main()
