from database.databases import database
from database.ApplyQuery import *
import pandas as pd
from dashbaord_ import QtWidgets,QtCore,Ui_MainWindow

def create_tables():
    Query(database,col=database["columns"],query=CREATE)
def insert_into_database(row):
    Query(database,col=database["columns"],query=INSERT,value=row)
def select_database(where_list=None,where_values=None):
    if where_list == None:
        data = Query(database,col=database["columns"],query=SELECT)
    else:
        data = Query(database,col=database["columns"],query=SELECT,where=where_list,value=where_values)
    if data:
        rows = [list(row) for row in data]
        return pd.DataFrame(rows,columns = database["columns"])
    else:
        return None

def local_db():
    create_tables()
    file = "database/Current Dashboard Data.xlsx"
    df = pd.read_excel(file)

    for row in range(1000):
        row_data = []
        for cols in df.columns:
            if cols == "active" or cols == "u_age_in_days" or cols == "child_incidents" or cols == "u_it_resolution":
                data = str(df[cols][row])
            else:
                data = df[cols][row]
            row_data.append(data)
        insert_into_database(row_data)


class ProgressBar(QtCore.QRunnable):
    def __init__(self, progressbar):
        QtCore.QRunnable.__init__(self)
        self.progressbar = progressbar
        
    def update(self,value):
        QtCore.QMetaObject.invokeMethod(self.progressbar, "setValue",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Q_ARG(int, value))

    