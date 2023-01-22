


import sys
from create_widget import checkbox
from imgs.back_ import *
from forcasting.forcaseting_wind import *





class start:
    def __init__(self) -> None:
        
        self.date_format = "%m/%d/%Y"
        self.status_loading = True
        self.filter_status = False

   
      

        self.window = Ui_MainWindow()
        self.window.setupUi(MainWindow)
        self.set_table()
        self.create_checkbox = checkbox()
        self.progress_change = ProgressBar(self.window.progressBar)
        self.FWind = Forcaseting_window()
        print("setting..")
        self.FWind.dot_img = self.window.forcasting_dot
        self.FWind.start_thread()
        self.FWind.forcasting_label = self.window.label_15
        
 
        MainWindow.show()
        
        self.filters = [[],[],[],[]]
        # Plots
        self.plots_list = [self.window.daily_trend_plot,self.window.by_priority_plot,self.window.by_type_plot,self.window.by_state_plot,self.window.generated_by_plot]
        self.FWind.forcasting_plot_list = [self.window.daily_trend_plot_2,self.window.by_priority_plot_2,self.window.by_type_plot_2,self.window.by_state_plot_2,self.window.generated_by_plot_2]

        # Incident State Checkboxes list
        self.states_check_list = [self.window.in_progress_check,self.window.new_check,self.window.on_hold_check,self.window.resolved_check]
        self.FWind.f_states_check_list = [self.window.in_progress_check_2,self.window.new_check_2,self.window.on_hold_check_2,self.window.resolved_check_2]

        # Type Check List
        self.type_check_list = [self.window.request_type_check,self.window.restoration_type_check]
        self.FWind.f_type_check_list = [self.window.request_type_check_2,self.window.restoration_type_check_2]
        self.update = False

      
        
        # Dates
        self.date_list = [self.window.dateEdit,self.window.dateEdit_2]

        self.window.dateEdit_3.setDateTime(QtCore.QDateTime(QtCore.QDate.fromString(self.FWind.today_date,"yyyy-MM-dd"), QtCore.QTime.fromString(self.FWind.today_time,"H:M:S")))
        self.window.dateEdit_3.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate.fromString(self.FWind.today_date,"yyyy-MM-dd"), QtCore.QTime.fromString(self.FWind.today_time,"H:M:S")))
        self.window.dateEdit_3.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate.fromString(self.FWind.f_date,"yyyy-MM-dd"), QtCore.QTime.fromString(self.FWind.f_time,"H:M:S")))

        self.window.dateEdit_4.setDateTime(QtCore.QDateTime(QtCore.QDate.fromString(self.FWind.f_date,"yyyy-MM-dd"), QtCore.QTime.fromString(self.FWind.f_time,"H:M:S")))
        self.window.dateEdit_4.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate.fromString(self.FWind.today_date,"yyyy-MM-dd"), QtCore.QTime.fromString(self.FWind.today_time,"H:M:S")))
        self.window.dateEdit_4.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate.fromString(self.FWind.f_date,"yyyy-MM-dd"), QtCore.QTime.fromString(self.FWind.f_time,"H:M:S")))

        self.FWind.f_date_list = [self.window.dateEdit_3,self.window.dateEdit_4]
        for dated in range(len(self.date_list)):
            self.date_list[dated].dateChanged.connect(lambda event:self.date_change(event))
        for dated in range(len(self.FWind.f_date_list)):
            self.FWind.f_date_list[dated].dateChanged.connect(lambda event:self.FWind.change_date(event))
        
        self.fetch_data()


    def setting_up_loading(self):
        c = 0
        while self.status_loading:
            if c == 0:
                c = 1
                text = "Setting Up Data"
            elif c == 1:
                c = 2
                text = "Setting Up Data."
            elif c == 2:
                c = 3
                text = "Setting Up Data.."
            else:
                text = "Setting Up Data..."
                c = 0
            self.window.status_label.setText(text)
            time.sleep(0.2)
        self.progress_change.update(35)
    def initialize(self,date=False):
        if self.update:
            self.window.progressBar.show()
        
        self.status_loading = True
        if date:
            self.window.status_label.setText("Getting Calender Date")
            self.progress_change.update(30)
            self.get_date_interval()
            
        
        thread = Thread(target=self.setting_up_loading)
        thread.start()
      
        threadClass = Worker(filter_status=self.filter_status,filters=self.filters,start_date=self.start_date,end_date=self.end_date,db_data=self.db_data)
        threadClass.signal.final_data.connect(self.plot)
        threadClass.signal.plot_data.connect(self.insert_into_table)
        self.FWind.pool.start(threadClass)
    
     
    def set_table(self):
        for cols in range(self.window.data_table.columnCount()):
            self.window.data_table.setColumnWidth(cols,200)
        
    def toggled_filter(self,event,x,text,state):
        print("Filter Text: ",text)
        print(f"{text} Filter Checked: ",state.isChecked())
        if state.isChecked():
            if text not in self.filters[x]:
                self.filters[x].append(text)
                self.filter_status = True
                print(f"Applied Filter: {text}")
        else:
            if text in self.filters[x]:
                self.filters[x].remove(text)
                if len(self.filters[x]) == 0:
                    self.filter_status = False
                print(f"Removed Filter: {text}")
        print("Total Filters: ",self.filters)
        
        self.update = True
        self.initialize()

    def create_age_group_checkboxes(self,db_data):
        self.FWind.forcasting_func(db_data)
        
        self.window.status_label.setText("Creating Filters")
        self.progress_change.update(20)
        age_check_frames = [self.window.scrollAreaWidgetContents_2,self.window.scrollAreaWidgetContents_5]
        age_check_layout = [self.window.verticalLayout_5,self.window.verticalLayout_13]
        self.age_group_check_list = []
        self.f_age_check_list = []
        self.db_data = db_data
        for i in range(2):
            if i == 0:
                l = self.age_group_check_list
            else:
                l = self.f_age_check_list
            for value in db_data["Age_Group"].unique():
                l.append(self.create_checkbox.create(frame=age_check_frames[i],text=value,layout=age_check_layout[i]))
        self.assigned_to_list = []
        self.f_assigned_to_list = []
        assigned_to_frames = [self.window.scrollAreaWidgetContents_3,self.window.scrollAreaWidgetContents_6]
        assigned_to_layout = [self.window.verticalLayout_7,self.window.verticalLayout_15]
        for i in range(2):
            if i == 0:
                l = self.assigned_to_list
            else:
                l = self.f_assigned_to_list
            for value in db_data["assigned_to"].unique():
                l.append(self.create_checkbox.create(frame=assigned_to_frames[i],text=value,layout=assigned_to_layout[i])) 
       
        all_filter_checks = [self.states_check_list,self.age_group_check_list,self.type_check_list,self.assigned_to_list]
        f_all_filters = [self.FWind.f_states_check_list,self.f_age_check_list,self.FWind.f_type_check_list,self.f_assigned_to_list]
       
        x = 0
        print("Start connecting lists")
        for lists in f_all_filters :
            for check in lists:
                check.stateChanged.connect(lambda event,i=x,text = check.text(),state=check:self.FWind.filter_toggled(event,i,text,state))
            x += 1
        x = 0
        for lists in all_filter_checks :
            for check in lists:
                check.stateChanged.connect(lambda event,i=x,text = check.text(),state=check:self.toggled_filter(event,i,text,state))
            x += 1
        self.initialize(date=True)
      
    def date_change(self,event):
        self.update = True
        self.initialize(date=True)

    def get_date_interval(self):
        """
        Function to get value of Start & End Time Calender
        """
        self.FWind.get_date_interval()
        self.start_date =datetime.datetime.strptime(self.date_list[0].date().toPyDate().strftime(self.date_format),self.date_format).date()
        self.end_date = datetime.datetime.strptime(self.date_list[1].date().toPyDate().strftime(self.date_format),self.date_format).date()
        print("Start Date: ",self.start_date," End Date: ",self.end_date)
   

   
   

    def fetch_data(self):
        self.window.progressBar.show()
        
        self.window.status_label.setText("Loading Database")
        self.progress_change.update(10)
        threadClass = db_Class()
        threadClass.dbsignal.db_data.connect(self.create_age_group_checkboxes)
        self.FWind.pool.start(threadClass)
     

    



    def plot(self,final_data):
        
        self.status_loading = False
        self.window.status_label.setText("Plotting Graphs")
        self.progress_change.update(50)
        if len(final_data[0].index) == 0:
            error_dialog("Data Error","No Data Found for applied filter","")
            return None
        count = 0
        prog_count = 50
        if not self.update:
            self.sc_list = []
            self.graph_list = []
        for graph in self.plots_list:
            if not self.update:
                sc = MplCanvas(self, title=self.FWind.t[count])
                sc_option = sc
            else:
                self.sc_list[count].axes.clear()
                sc_option = self.sc_list[count]
            if count == 0:
                
                graph_value = final_data[count].plot(ax=sc_option.axes,kind="bar")    
                 
                
                positions = [0,len(final_data[count].index)//3,len(final_data[count].index)//2,int(len(final_data[count].index)//1.2),len(final_data[count].index)-1]
                xlbls = [str(final_data[count].index[i]).split(" ")[0] for i in positions]
                if self.update:
                    self.graph_list[count].set_xticks(positions)
                    self.graph_list[count].set_xticklabels(xlbls,rotation=15)
                else:
                    graph_value.set_xticks(positions)
                    graph_value.set_xticklabels(xlbls,rotation=15)
                    sc.axes.legend(loc='upper left',ncol=3)
                    sc.axes.set_ylabel("Count of Assignment Group")
                    sc.axes.set_xlabel("System Updated On")
            else:
                df = final_data[count][self.FWind.y[count]].value_counts()
                graph_value = df.plot.pie(ax=sc_option.axes,ylabel='',labeldistance=None)
                if not self.update:
                    graph_value.legend(bbox_to_anchor=(0.64, 1.05), loc='upper left')
                else:
                    self.graph_list[count].legend(bbox_to_anchor=(0.64, 1.05), loc='upper left')
            if self.update:
                self.sc_list[count].draw()
                self.sc_list[count].flush_events()
            else:
 
                # self.plotted.append(graph_value)
                layout = QtWidgets.QHBoxLayout(graph)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                layout.addWidget(sc_option)

                # self.plot_sc.append(self.sc)
            count += 1
            prog_count += 5
            self.progress_change.update(prog_count)
            if not self.update:
                self.sc_list.append(sc)
                self.graph_list.append(graph_value)
   
    def insert_into_table(self,plot_data):
        self.window.status_label.setText("Inserting Into Table")
        self.progress_change.update(90)
        self.window.data_table.setRowCount(0)

        cols = ["Incident_State","Incident_Type","Assignment_Group","short_description","assigned_to","closed_by","active","closed_at"]
        for rows in range(len(plot_data["sys_updated_on"])):

            self.window.data_table.setRowCount(self.window.data_table.rowCount()+1)
            col_count = 0
            for col in cols:
                try:
                    cell_data = str(plot_data[col][rows])
                except:
                    cell_data = " "

                item = QtWidgets.QLabel()
                item.setText(cell_data)
                item.setStyleSheet("color:white;\n"
                "background-color:rgb(60, 153, 85);\n")
                # item.setAlignment(Qt.AlignCenter)
         
                self.window.data_table.setCellWidget(rows, col_count, item)
                col_count += 1
        self.window.status_label.setText("Done")
        self.progress_change.update(100)
        self.window.progressBar.hide()
            



if __name__ == "__main__":
    # quo = queue.Queue()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()


    gui = start()



    sys.exit(app.exec_())
