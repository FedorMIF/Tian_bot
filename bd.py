import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def add_new_user(user_id, name):
    connection = create_connection("/home/fedor/Документы/Telegambot/user_data.sqlite")
    cur = connection.cursor()
    good = 'F'
    try:
        if give_user_name(user_id) == '':
            val = [(int(user_id), str(name))]
            cur.executemany("INSERT INTO users VALUES (?,?)", val)
            connection.commit()
            print(f"Add new user{user_id} aka {name} successful")
            good = 'T'
        else:
            print("Такой уже есть")
            connection.close()
            return "double"

    except Error as e:
        print(f"The error '{e}' occurred")
    
    connection.close()

    return good

def edit_user_name(user_id, name):
    connection = create_connection("/home/fedor/Документы/Telegambot/user_data.sqlite")
    cur = connection.cursor()
    good = False
    try:
        val = [(str(name), int(user_id))]
        cur.executemany("UPDATE users SET name = ? WHERE id = ?", val)
        connection.commit()
        print(f"Edit new user{user_id} aka {name} successful")
        good = True

    except Error as e:
        print(f"The error '{e}' occurred")
        
    connection.close()

    return good

def create_new_bdrasp(user_id):
    connection = create_connection("/home/fedor/Документы/Telegambot/user_data.sqlite")
    cur = connection.cursor()
    good = False
    try:
        cur.execute(f"CREATE TABLE user{user_id} ( name text, time text)")
        connection.commit()
        print(f"Connection to {user_id} DB successful")
        good = True

    except Error as e:
        print(f"The error '{e}' occurred")
        
    connection.close()
    return good

def give_user_name(user_id):
    connection = create_connection("/home/fedor/Документы/Telegambot/user_data.sqlite")
    cur = connection.cursor()
    good = False
    name = 'err'
    try:
        cur.execute(f"SELECT name FROM users WHERE id = '{user_id}'")
        connection.commit()
        mess = cur.fetchall()
        name_row = ''.join(str(x) for x in mess)
        name = ''
        i = 0
        for i in range(0, len(name_row)): 
            if name_row[i] == ('('): 
                continue
            elif name_row[i] == (','): 
                continue 
            elif name_row[i] == ("'"): 
                continue
            elif name_row[i] == (')'): 
                continue
            name += name_row[i]   
            

        
        #print(cur.fetchall())
        good = True

    except Error as e:
        print(f"The error '{e}' occurred")
    
    connection.close()
    if good:
        return name
    else:
        return False

def add_new_rasp(user_id, data, note):
    connection = create_connection("/home/fedor/Документы/Telegambot/user_data.sqlite")
    cur = connection.cursor()
    good = False
    try:
        cur.execute(f"INSERT INTO user{user_id} VALUES ('{note}', '{data}')")
        connection.commit()
        print(f"Add new rasp to user{user_id}: {note}, {data} successful")
        good = True

    except Error as e:
        print(f"The error '{e}' occurred")
    
    connection.close()

    return good
