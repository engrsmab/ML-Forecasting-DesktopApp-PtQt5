
from PyQt5.QtCore import pyqtSlot as Slot,QThreadPool,QRunnable,QObject,pyqtSignal
import pandas as pd
import datetime
from backend import *

# global window_frame

class dbSignal(QObject):
    db_data = pyqtSignal(pd.DataFrame)
    forcasted_data = pyqtSignal(list)
    training_label = pyqtSignal(str)

class db_Class(QRunnable):
    def __init__(self) -> None:
        super().__init__()
        self.dbsignal = dbSignal()
    @Slot()
    def run(self):
        db_data = select_database()
        self.dbsignal.db_data.emit(db_data)

class forcaseting_thread(QRunnable):
    def __init__(self,forcasting_class) -> None:
        super().__init__()
        self.signal = dbSignal()
        self.forc_class = forcasting_class

    @Slot()
    def run(self):
        self.forc_class.tokenize()
        self.forc_class.training()
        self.signal.training_label.emit("Predicting Data")

class prediction_thread(QRunnable):
    def __init__(self,forecasting_class,filter_data) -> None:
        super().__init__()
        self.signal = dbSignal()
        self.forc_class = forecasting_class
        self.filter_data = filter_data

    @Slot()
    def run(self):
        self.forc_class.predict(self.filter_data)
        self.signal.forcasted_data.emit(self.forc_class.final_data)



class Signals(QObject):
    final_data = pyqtSignal(list,list)
    plot_data = pyqtSignal(pd.DataFrame)

class Worker(QRunnable):
    def __init__(self,filters,filter_status,start_date,end_date,db_data) -> None:
        super().__init__()
        self.signal = Signals()
 
        self.date_format = "%m/%d/%Y"
        self.start_date = start_date
        self.end_date = end_date
        self.db_data = db_data
        self.filters = filters
        self.filter_status = filter_status

    @Slot()
    def run(self):
        
        self.setting_plot_data()

        self.signal.final_data.emit(self.final_data,self.group_list)
        self.signal.plot_data.emit(self.plot_data)

    def setting_plot_data(self):

        self.db_data.notna()     # removing rows having empty cells
        self.plot_data = self.db_data
        self.plot_data["sys_updated_on"] = pd.to_datetime(self.plot_data["sys_updated_on"])
        self.plot_data.sort_values(by="sys_updated_on")

        filter_heading = ["Incident_State","Age_Group","Incident_Type","assigned_to"]   # columns on which we want to filter the whole data upon these
        if self.filter_status:
            x = 0
            for list_data in self.filters:   # it has 4 further lists having applied filters
                    # it unfolds filter lists one by one
                    i = 0
                    print("list data: ",list_data)

                    for value in self.plot_data[filter_heading[x]]:     # interating through columns of datasheet one by one

                        if (len(list_data) > 0) and (value not in list_data):   # if value of datasheet is equal to selected filter value then drop that row
                            self.plot_data = self.plot_data.drop(i) 
                        i += 1 
                    x += 1

                    self.plot_data = self.plot_data.reset_index(drop=True)  # this drop=True drops the replaces the index column with new
              
                            

                       
                
        print("len of plot data: ",len(self.plot_data["sys_updated_on"]))
        for date in range(len(self.plot_data["sys_updated_on"])):   # filtering the rest of datasheet depanding upon selected dates
    
            if (datetime.datetime.strptime(self.plot_data["Sys_Updated_on_2"][date], self.date_format).date() - self.start_date).days >= 0 and (self.end_date - datetime.datetime.strptime(self.plot_data["Sys_Updated_on_2"][date],self.date_format).date()).days >= 0:
                pass
            else:
                self.plot_data = self.plot_data.drop(date)
        self.plot_data = self.plot_data.reset_index(drop=True)
        print("len after date set: ",len(self.plot_data["sys_updated_on"]))   
        
        y_list = []
        x_list = self.plot_data["Sys_Updated_on_2"].unique()
        assignment_group_list = self.plot_data["Assignment_Group"].unique()
        self.group_list = list(assignment_group_list)

        loop = 0
        for value in x_list:
            counter = []
            data = self.plot_data[self.plot_data["Sys_Updated_on_2"] == value]
            data = data["Assignment_Group"].value_counts()
            for group in assignment_group_list:
                try:
                    counter.append(data[group])
                except:
                    counter.append(0)
                # found_group.append(data[group])
            loop += 1
            if loop > len(assignment_group_list):
                self.group_list.append(0)
            y_list.append(counter)
        
        print("Group Counting Done!!!")

        self.final_data = []
        graph = {}

        # Saperating each group value into lists

        for group in range(len(assignment_group_list)):
            temp_list = []
            for list_ in y_list:
                temp_list.append(list_[group])
            graph[assignment_group_list[group]] = temp_list

        self.final_data.append(pd.DataFrame(graph,index=x_list))

        
        graph_2 = {}
        graph_2["priority_value"] = self.plot_data["Priority"]

 
        self.final_data.append(pd.DataFrame.from_dict(graph_2))

        
        graph_3 = {}
        graph_3["state_value"] = self.plot_data["Incident_State"]
        self.final_data.append(pd.DataFrame.from_dict(graph_3))
        
        graph_4 = {}
        graph_4["type_value"] = self.plot_data["Incident_Type"]
        self.final_data.append(pd.DataFrame.from_dict(graph_4))
        
        graph_5 = {}
        graph_5["generated_value"] = self.plot_data["Generated_by"]
        self.final_data.append(pd.DataFrame.from_dict(graph_5))


    
