import pandas as pd
import numpy as np
import datetime
df = {}
df['Name'] = ['AM ETL OPERATIONS', 'AM ETL OPERATIONS', 'AM ETL OPERATIONS','Jim','Harry','Ben',0]
df['TotalMarks'] = [82, 38, 63,22,55,40,9]
df['Grade'] = ['A', 'E', 'B','E','C','D','E']
df['Promoted'] = [True, False,True,False,True,True,True]
names = ['John', 'Doe', 'Bill']
df = pd.DataFrame(df)
df = df['Name'].value_counts()
print(df)

# df = {"Name":['John', 'Doe', 'Bill','Jim','Harry','Ben']}
# df = pd.DataFrame(df,index=['A', 'E', 'B','E','C','D'])
# v = df.index[0]
# print(v)
# date = datetime.datetime.now()
# today_date = datetime.datetime.now().strftime("%Y-%m-%d")
# today_time = datetime.datetime.now().strftime("%H:%M:%S")
# f_date = datetime.timedelta(days=60)
# print(today_date,today_time,(date + f_date).strftime("%Y-%m-%d"))


