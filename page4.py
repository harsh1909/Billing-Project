from PyQt5.QtWidgets import *
import page1,database
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt,QSize,QDate

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
plt.style.use(['dark_background'])




from collections import defaultdict

class page_profit(QWidget):


    def __init__(self,m):
        super().__init__(m)
        self.m = m
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.graph = None
        self.home_btn= QPushButton("Home",self)
        
        self.home_btn.clicked.connect(self.on_click_home)
        self.mainLayout.addWidget(self.home_btn)
        




        #self.mainLayout.addWidget(profit_details(self))
        self.scrollArea = QScrollArea(self)
        self.scrollAreaWidget = profit_details(self)        
        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.mainLayout.addWidget(self.scrollArea)


    
        self.setLayout(self.mainLayout)

    def on_click_home(self):
        print("go to home")
        self.m.setCentralWidget(page1.home_page(self.m))
        self.m.setWindowTitle("Home")



class profit_details(QWidget):


    def __init__(self,m):
        super().__init__(m)
        self.m = m
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignLeft)

        date = QDate.currentDate().toString(Qt.ISODate)

        self.day = day_widget(self,self.m,"Day","YYYY-MM-DD")
        self.mainLayout.addWidget(self.day)

        self.month = day_widget(self,self.m,"Month","YYYY-MM")
        self.mainLayout.addWidget(self.month)

        self.year = day_widget(self,self.m,"Year","YYYY")
        self.mainLayout.addWidget(self.year)
        

    
        self.setLayout(self.mainLayout)




class day_widget(QWidget):
    def __init__(self,m,primary,period,placeholder):
        super().__init__(m)
        self.m = m
        self.primary = primary
        self.period = period
        self.placeholder = placeholder

        self.mainLayout = QHBoxLayout()

        self.profit_details = QGroupBox("Profit Details By "+self.period)

        self.form_details = QFormLayout()

        self.set_up()

        self.profit_details.setLayout(self.form_details)

        self.mainLayout.addWidget(self.profit_details)
        self.setLayout(self.mainLayout)


    def set_up(self):
        self.date = QDate.currentDate().toString(Qt.ISODate) + "%"

        if self.period=="Month":
            self.date= self.date[:7] + "%"

        elif self.period=="Year":
            self.date= self.date[:4] + "%"

        print(self.date)


        self.input_date = QLineEdit()
        self.setFixedWidth(500)
        self.input_date.setPlaceholderText(self.placeholder)
        self.input_date.setText(self.date[:-1])
        self.details_btn = QPushButton("Details",self)
        self.details_btn.clicked.connect(self.on_click_details)

        choice = database.get_list("vehicle_no")
        choice.insert(0,"Net Profit")

        self.choice_graph_btn = QComboBox()
        self.choice_graph_btn.addItems(choice)
        #self.net_graph_btn.clicked.connect(self.on_click_net_Graph)

        self.view_graph_btn = QPushButton("View Graph",self)
        self.view_graph_btn.clicked.connect(self.on_click_view_Graph)

        self.total_profit = QLabel(database.get_total_profit_of_day(self.date))

        self.form_details.addRow(self.input_date , self.choice_graph_btn)
        self.form_details.addRow(self.details_btn , self.view_graph_btn)
        self.form_details.addRow(QLabel("Total profit of the "+self.period+" : "),self.total_profit)

        self.set_up_vehicle_details(self.date)

    def set_up_vehicle_details(self,date):
        self.vehicle_no = []
        self.vehicle_profit = []

        self.data = database.get_total_profit_of_day_details(date)

        for r in self.data:
            self.vehicle_no.append(QLabel(r[0]))
            self.vehicle_profit.append(QLabel(str(r[1])))

        for i in range(len(self.vehicle_no)):
            self.form_details.addRow(self.vehicle_no[i],self.vehicle_profit[i])






    def on_click_details(self):
        print(self.form_details.rowCount())
        for i in range(3,self.form_details.rowCount()):
            self.form_details.removeRow(3)

        if len(self.input_date.text())==0:
            self.total_profit.setText(database.get_total_profit_of_day(self.date))
            self.set_up_vehicle_details(self.date)
        else:
            self.total_profit.setText(database.get_total_profit_of_day(self.input_date.text()+"%"))
            self.set_up_vehicle_details(self.input_date.text()+"%")
    	



    def on_click_view_Graph(self):
        print("vehicle graph clicked")
        if self.primary.graph!=None:
            self.primary.mainLayout.removeWidget(self.primary.graph)
            self.primary.graph.deleteLater()
            self.primary.graph = None
        
        self.primary.graph = PlotCanvas(self,self.choice_graph_btn.currentText())

        self.primary.mainLayout.addWidget(self.primary.graph)



class PlotCanvas(FigureCanvas):

    def __init__(self, parent, choice):
        self.parent = parent
        fig = Figure(figsize=(5, 4), dpi=100)   #width,height,dpi
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        if choice=="Net Profit":
            self.plot_net_profit()

        else:self.plot_vehicle_profit(choice)


    def plot_net_profit(self):
        
        date = self.parent.input_date.text()
        #print(date)

        if self.parent.period=="Month":
            res = database.get_total_profit_of_per_day_details(date[:-2]+"%")

        elif self.parent.period=="Year":
            res = database.get_total_profit_of_per_day_details("%")

        else:

            res = database.get_total_profit_of_per_day_details(date[:-2]+"%")
        #print(res)
        xg,yg = self.process_res(res)
        self.plot_graph(xg,yg)

    def plot_vehicle_profit(self,vehicle_no):
        
        date = self.parent.input_date.text()
        print(vehicle_no)

        if self.parent.period=="Month":
            res = database.get_total_profit_of_per_day_vehicle_details(date[:-2]+"%",vehicle_no)

        elif self.parent.period=="Year":
            res = database.get_total_profit_of_per_day_vehicle_details("%",vehicle_no)

        else:

            res = database.get_total_profit_of_per_day_vehicle_details(date[:-2]+"%",vehicle_no)
        #print(res)
        xg,yg = self.process_res(res)
        self.plot_graph(xg,yg)




    def process_res(self,res):
        xg,yg = [],[]

        if self.parent.period=="Day":
        
            for i in res:
                xg.append(int(i[0][8:]))
                yg.append(i[1])

        elif self.parent.period=="Month":
            map = defaultdict(lambda:0)

            for i in res:
                map[i[0][5:7]] += i[1]

            for i in map:
                xg.append(int(i))
                yg.append(map[i])

        else:
            map = defaultdict(lambda:0)

            for i in res:
                map[i[0][:4]] += i[1]

            for i in map:
                xg.append(int(i))
                yg.append(map[i])
        


        return xg,yg


    def plot_graph(self,xg,yg):

        print(xg,yg)

        #plt.plot([1, 2, 3, 4])
        #plt.ylabel('some numbers')
        #plt.show()

        #data = [random.random() for i in range(25)]
        #print(data)
        ax = self.figure.add_subplot(111)
        ax.plot(xg, yg,'go-')
        ax.set_ylabel("Profit (Rs)")
        ax.set_xlabel("Time Period ("+self.parent.period+"s)")
        #ax.minorticks_off()
        #ax.axis([0,5,0,5])  [xmin, xmax, ymin, ymax]

        #for a,b in zip(xg, yg): 
        #    ax.text(a, b, str(b))

        for i,j in zip(xg,yg):
            ax.annotate(str(j)+","+str(i),xy=(i,j))

        ax.set_title('Revenue Report')
        self.draw()