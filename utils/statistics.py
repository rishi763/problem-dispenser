import sqlite3
cursor=None
connection=None

def main():
    global cursor
    global connection
    connection=sqlite3.connect('data/statistics.db')
    connection.execute('''CREATE TABLE IF NOT EXISTS STATISTICS
         (ID                    INT     PRIMARY KEY     NOT NULL,
         CACHED_NAME            VARCHAR(32),
         CACHED_DISCRIMINATOR   CHAR(4),
         PUBLIC                 BOOL,
         AMC_8_SOLVED           INT,  
         AMC_10_SOLVED          INT,
         AMC_12_SOLVED          INT,
         AHSME_SOLVED           INT,
         AIME_SOLVED            INT,
         CALT_SOLVED            INT,
         SMC_SOLVED             INT,
         TOTAL_SOLVED           INT,
         AMC_8_FAILED           INT,
         AMC_10_FAILED          INT,
         AMC_12_FAILED          INT,
         AHSME_FAILED           INT,
         AIME_FAILED            INT,
         CALT_FAILED            INT,
         SMC_FAILED             INT, 
         TOTAL_FAILED           INT,  
         AMC_8_RATING           DECIMAL(18,1),
         AMC_10_RATING          DECIMAL(18,1),
         AMC_12_RATING          DECIMAL(18,1),
         AIME_RATING            DECIMAL(18,1),
         TOTAL_RATING           DECIMAL(18,2)) 
         ''')
    cursor=connection.cursor()

def get_position(id, section):
    cursor.execute("SELECT ID, PUBLIC FROM STATISTICS ORDER BY "+section+" DESC")
    positions=[x[0] for x in cursor.fetchall() if x[1]]
    if id in positions: 
        return positions.index(id)+1
    else:
        return -1

def add_user(id,name,discriminator):
    cursor.execute("INSERT INTO STATISTICS (ID,CACHED_NAME,CACHED_DISCRIMINATOR,PUBLIC,AMC_8_SOLVED,AMC_10_SOLVED,AMC_12_SOLVED,AIME_SOLVED,CALT_SOLVED,SMC_SOLVED,TOTAL_SOLVED,AMC_8_FAILED,AMC_10_FAILED,AMC_12_FAILED,AIME_FAILED,CALT_FAILED,SMC_FAILED,TOTAL_FAILED,AMC_8_RATING,AMC_10_RATING,AMC_12_RATING,AIME_RATING,TOTAL_RATING)\
        VALUES(?,?,?,TRUE,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)", (id,name,discriminator))
    connection.commit()

def print_user(id):
    cursor.execute("SELECT * FROM STATISTICS WHERE ID=?",(id,))
    print(cursor.fetchall())

def print_all_users():
    cursor.execute("SELECT * FROM STATISTICS")
    users=cursor.fetchall()
    for user in users:
        print(user)

def user_exists(id):
    cursor.execute("SELECT * FROM STATISTICS WHERE ID=?",(id,))
    return cursor.fetchall()!=[]

def delete_user(id):
    cursor.execute("DELETE FROM STATISTICS WHERE ID=?",(id,))
    connection.commit()

def get_user_id(name, discriminator):
    cursor.execute("SELECT ID FROM STATISTICS WHERE CACHED_NAME=? AND CACHED_DISCRIMINATOR=?",(name,discriminator))
    id=cursor.fetchone()
    if id!=None:
        return id[0]
    else:
        return None

def get_cached_name(id):
    cursor.execute("SELECT CACHED_NAME,CACHED_DISCRIMINATOR FROM STATISTICS WHERE ID=?",(id,))
    name=cursor.fetchone()
    if name[0]!=None:
        return name[0]+"#"+name[1]
    else:
        return None

def set_name(id,name,discriminator):
    cursor.execute("UPDATE STATISTICS SET CACHED_NAME=?, CACHED_DISCRIMINATOR=? WHERE ID=?",(name,discriminator,id))
    connection.commit()

def set_public(id, public):
    cursor.execute("UPDATE STATISTICS SET PUBLIC=? WHERE ID=?",(public, id))
    connection.commit()

def get_public(id):
    cursor.execute("SELECT PUBLIC FROM STATISTICS WHERE ID=?",(id,))
    return bool(cursor.fetchone()[0])

def get_stats(id):
    cursor.execute("SELECT AMC_8_SOLVED,AMC_10_SOLVED,AMC_12_SOLVED,AIME_SOLVED,CALT_SOLVED,SMC_SOLVED,TOTAL_SOLVED,AMC_8_FAILED,AMC_10_FAILED,AMC_12_FAILED,AIME_FAILED,CALT_FAILED,SMC_FAILED,TOTAL_FAILED,AMC_8_RATING,AMC_10_RATING,AMC_12_RATING,AIME_RATING,TOTAL_RATING FROM STATISTICS WHERE ID=?",(id,))
    user_data=cursor.fetchall()
    if user_data!=[]:
        user_data=[round(x,2) if type(x)==float else x for x in list(user_data[0])]
    else:
        return None
    index=0
    stats=[]
    for section in [x[0] for x in cursor.description]:
        stats.append(centerify(str(user_data[index]),6)) 
        if "SOLVED" in section or "RATING" in section:
            stats.append(centerify(str(get_position(id,section)),3))
        index+=1
    return stats

def get_leaderboard(section):
    cursor.execute("SELECT ID, PUBLIC,"+section+" FROM STATISTICS ORDER BY "+section+" DESC")
    return [[x[0],round(x[2],2)] for x in cursor.fetchall() if x[2]!=0 and x[1]]

def update_values(id,values,name,discriminator):
    if not user_exists(id):
        add_user(id,name,discriminator)
    for key in values:
        cursor.execute("UPDATE STATISTICS SET "+key+" = "+key+"+ ? WHERE ID=?",(values[key],id))
    connection.commit()

def centerify(string, length):
    whitespace=length-len(string)
    return  " "*(whitespace//2)+string+" "*(whitespace//2+whitespace%2)
    
main()


"""stats=open("stats.csv","r")
for i in range(200):
    data=stats.readline().split(',')
    for i in range(len(data)):
        try:
            data[i]=int(data[i])
        except:
            data[i]=float(data[i])
    cursor.execute("INSERT INTO STATISTICS VALUES(?,NULL,NULL,FALSE,0,?,?,?,0,0,?,0,0,0,0,0,0,0,0,?,?,?,?)",(data[0],data[2],data[3],data[4],data[1],data[-4],data[-3],data[-2],data[-1]))
connection.commit()"""