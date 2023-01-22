import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import numpy,datetime,random
class forcasting:
    def __init__(self) -> None:
        
        # path = "database/Current Dashboard Data.xlsx"
        # # spacy_nlp = spacy.load('en_core_web_sm')
        # self.df = pd.read_excel(path)
        self.df = None
        self.date = datetime.datetime.now()
        self.today_date = self.date.strftime("%Y-%m-%d")
        self.date_format = "%m/%d/%Y"
        self.date_interval = None
    def tokenize(self):
        self.training_cols = ["Incident_State","Age_Group","Incident_Type","assigned_to","Priority","Generated_by","Sys_Updated_on_2","Assignment_Group"]
        self.training_lists = []
        self.future_dates = []
        self.unique_groups = self.df["Assignment_Group"].unique()
        x = 0
        for col in self.training_cols:
            c = 0
            self.training_lists.append(self.df[col].unique())
            # self.df[col] = self.df[self.df[col] == None]
            for value in self.df[col].unique():
               
                self.df[col] = self.df[col].replace(str(value),str(c))
                c += 1
            
            if x == 1:
                for n in range(int(self.date_interval)*len(self.unique_groups)):
                    self.future_dates.append(c)
                    c += 1
            x += 1
        self.group_list = self.training_lists[-1]
        self.training_lists.pop(-1)
        self.training_cols.pop(-1)


    def training(self):
         
        self.X = self.df[self.training_cols]
 
        self.Y = self.df["Assignment_Group"]
        self.X = preprocessing.StandardScaler().fit(self.X).transform(self.X.astype(float))

        X_train, X_test, y_train, self.y_test = train_test_split( self.X, self.Y, test_size=0.2, random_state=4)

        k = 4
        self.neigh = KNeighborsClassifier(n_neighbors = k).fit(X_train,y_train)
        # filtr = numpy.array([[1.0,float(n),0.0,2.0,1.0,1.0,4.0] for n in range(200)])
    def predict(self,filter_data):
        for c in range(4):
            x = 0
            for value in filter_data[c]:
                try:
                    filter_data[c][x] = float(self.training_cols[c].index(str(value)))
                except:
                    pass
                x += 1
            if len(filter_data[c]) == 0:
                filter_data[c].append(0.0)
        filtered_data = numpy.array([[filter_data[0][0],filter_data[1][0],filter_data[2][0],filter_data[3][0],1.0,1.0,self.future_dates[n]] for n in range(int(self.date_interval)*len(self.unique_groups))])
        yhat = self.neigh.predict(filtered_data)
        print("prediction: ",yhat)
        result = [self.group_list[int(x)] for x in yhat]
        final_result = []
        c = 0
        for i in range(int(self.date_interval)):
            inner_list = []
            for n in range(len(self.unique_groups)):
                inner_list.append(result[c])
                c += 1
            final_result.append(inner_list)
   
        # self.result = pd.DataFrame({"prediction":self.result})
        final_df = []
        for point in final_result:
            result_df = pd.DataFrame({"point":point})
            result_df = result_df["point"].value_counts()
        
            final_df.append(result_df)
        graph = {}
        for group in self.unique_groups:
            li = []
            for i in range(int(self.date_interval)):
                try:
                    li.append(final_df[i][group])
                except:
                    li.append(0)
            graph[group] = li
        x_list = [(self.date + datetime.timedelta(days=i)).strftime(self.date_format) for i in range(1,int(self.date_interval)+1)]
        graph = pd.DataFrame(graph,index=x_list)
        self.final_data = []
        self.final_data.append(graph)

        graph_2 = {}


            
        graph_2["priority_value"] = [self.training_lists[4][random.randint(0,len(self.training_lists[4])-1)] for i in range(int(self.date_interval))]

 
        self.final_data.append(pd.DataFrame.from_dict(graph_2))

        
        graph_3 = {}
        graph_3["state_value"] = [self.training_lists[0][int(filter_data[0][0])] for i in range(int(self.date_interval))]
        self.final_data.append(pd.DataFrame.from_dict(graph_3))
        
        graph_4 = {}
        graph_4["type_value"] = [self.training_lists[2][int(filter_data[2][0])] for i in range(int(self.date_interval))]
        self.final_data.append(pd.DataFrame.from_dict(graph_4))
        
        graph_5 = {}
        graph_5["generated_value"] = [self.training_lists[5][random.randint(0,len(self.training_lists[5])-1)] for i in range(int(self.date_interval))]
        self.final_data.append(pd.DataFrame.from_dict(graph_5))



        # print("Test set Accuracy: ", float(metrics.accuracy_score(self.y_test, yhat))*100)





