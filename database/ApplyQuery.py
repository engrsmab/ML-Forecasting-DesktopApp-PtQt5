import sqlite3
SELECT = "SELECT"
INSERT = "INSERT"
DELETE = "DELETE"
UPDATE = "UPDATE"
CREATE = "CREATE"
def Where_Query(value,exp):

    where_final = ""
    for i in range(len(value)):
        if i != 0:
            if exp == "del":
               where_final += " AND "
            else:
                where_final += ","
        where_final += str(value[i]) + "=?"
    return where_final
def Set_Columns(col,query):
        cols = ""
        unknowns = ""
        for i in range(len(col)):
            if i != 0:
                unknowns += ","
                cols += ","
            unknowns += " ? "
            if query != "CREATE":
                col[i] = col[i].split(" ")[0]
            cols += col[i]
        return cols,unknowns

def Query(parent,col=None, value=None, query=None,where=None):
    database = parent['database']
    table = parent['table']
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    if col != None:
        cols,unknowns = Set_Columns(col,query)
    else:
        cols = unknowns = ""

    if query == "INSERT":
        statement= f"INSERT INTO {table}({cols})VALUES({unknowns})"
    elif query == "CREATE":
        statement = f"CREATE TABLE IF NOT EXISTS {table}({cols})"
    elif query == "SELECT":
        if where != None:
           where_final = Where_Query(where,"del")
           statement = f"SELECT {cols} FROM {table} WHERE {where_final}"
        else:
            statement = f"SELECT {cols} FROM {table}"
    elif query == "UPDATE":
        cols_final = Where_Query(col,"=?")
        where_final = Where_Query(where,"del")
        statement = f"UPDATE {table} SET {cols_final} WHERE {where_final}"
    elif query == "DELETE":
        if where != None:
            where_final = Where_Query(where,"del")
            statement = f"DELETE FROM {table} WHERE {where_final}"
        else:
            statement = f"DELETE FROM {table}"
    else:
        statement = "NONE"
    # print(statement)
    result = "None"
    if statement != "NONE":
        # try:
        if query == "CREATE" or (query == "SELECT" and where == None) or (query == "DELETE" and where == None):
            cursor.execute(statement)
        else:
            cursor.execute(statement, value)
        if query == "SELECT":
            result = cursor.fetchall()
        else:
            result = "Done"
        
        # except sqlite3.Error as err:
        #     return err
    conn.commit()
    cursor.close()
    conn.close()
    return result