from problem.problem import Problem
import sqlite3

problem_dict={}
cursor=None
connection=None

def init():
    global cursor
    global connection
    global problem_dict
    connection=sqlite3.connect('data/problem_dict.db')
    connection.execute('''CREATE TABLE IF NOT EXISTS PROBLEM_DICT
         (ID            INT     PRIMARY KEY     NOT NULL,
         YEAR           INT,
         CONTEST        VARCHAR(8),
         VERSION        VARCHAR(8),
         NUMBER         INT, 
         DIFFICULTY     VARCHAR(8),
         ATTEMPTS       INT, 
         START_TIME     FLOAT)
         ''')
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM PROBLEM_DICT")
    for problem_data in cursor.fetchall():
        problem_dict[problem_data[0]]=Problem(dict={"year":problem_data[1],"contest":problem_data[2],"version":problem_data[3],"number":problem_data[4],"difficulty":problem_data[5],"attempts":problem_data[6],"start_time":problem_data[7]})

def get(id):
    global problem_dict
    return problem_dict.get(id)

def is_in(id):
    global problem_dict
    return id in problem_dict

def add(id, problem):
    global problem_dict
    global cursor
    global connection
    if not is_in(id):
        problem_dict[id]=problem
        cursor.execute("INSERT INTO PROBLEM_DICT (ID, YEAR, CONTEST, VERSION, NUMBER, DIFFICULTY, ATTEMPTS, START_TIME ) VALUES (?,?,?,?,?,?,?,?)",(id, problem.year, problem.contest, problem.version, problem.number, problem.difficulty, problem.attempts, problem.start_time))
        connection.commit()
        return 0
    else:
        return None

def remove(id):
    global problem_dict
    global cursor
    global connection
    if problem_dict.pop(id, None) is None:
        return None
    else:
        cursor.execute("DELETE FROM PROBLEM_DICT WHERE ID=?",(id,))
        connection.commit()
        return 0

def lower_attempts(id):
    global cursor
    global connection
    problem=get(id)
    problem.attempts-=1
    cursor.execute("UPDATE PROBLEM_DICT SET ATTEMPTS=ATTEMPTS-1 WHERE ID=?",(id,))
    connection.commit()
init()