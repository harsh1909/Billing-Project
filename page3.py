from PyQt5.QtWidgets import *
import page1,database
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt,QSize

class page_view(QWidget):


    def __init__(self,m):
        super().__init__(m)
        self.m  = m 
        self.descScrollArea = None
        self.scrollArea = None
        self.record=database.extract_records()

        self.mainLayout = QVBoxLayout()

        self.top = top_widget(self)
        
        self.mainLayout.addWidget(self.top)
        
        self.set_scroll_area(self.record)

        self.setLayout(self.mainLayout)

    
        
    def on_click_home(self):
            print("go to home")
            self.m.setCentralWidget(page1.home_page(self.m))
            self.m.setWindowTitle("Home")
            
            
    def set_scroll_area(self,record):
        self.scrollArea = QScrollArea(self)
        self.scrollAreaWidget = record_view(self,record)        
        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.mainLayout.addWidget(self.scrollArea)

    def set_desc_scroll_area(self,id):
        self.descScrollArea = QScrollArea(self)
        self.descScrollAreaWidget = desc_view(self,id)        
        self.descScrollArea.setWidget(self.descScrollAreaWidget)
        self.mainLayout.addWidget(self.descScrollArea)


    def on_click_record_row(self,id):
        if self.scrollArea!=None:
            self.mainLayout.removeWidget(self.scrollArea)
            self.scrollArea.deleteLater()
            self.scrollArea = None
        self.set_desc_scroll_area(id)


class top_widget(QWidget):
    def __init__(self,m):
        super().__init__(m)
        self.m = m
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignLeft)
        self.setFixedWidth(700)
        
        choice = ["trip_date","vehicle_no","material","driver_name","mechanic_name"]
        self.filter = QComboBox()
        self.filter.addItems(choice)
        self.filter.currentIndexChanged.connect(self.on_change_choice_btn)
        
        self.input_label = QLineEdit()
        self.input_label.setFixedWidth(200)
        self.input_label.setAlignment(Qt.AlignLeft)
        
        self.on_change_choice_btn()
        
        self.view_btn = QPushButton("View",self)
        self.view_btn.clicked.connect(self.on_click_view_btn)
        
        self.home_btn= QPushButton("Home",self)
        self.home_btn.clicked.connect(self.m.on_click_home)
        
        self.back_btn= QPushButton("Back",self)
        self.back_btn.clicked.connect(self.on_click_view_btn)
        
        
        self.mainLayout.addWidget(self.filter)
        self.mainLayout.addWidget(self.input_label)
        self.mainLayout.addWidget(self.view_btn)
        self.mainLayout.addWidget(self.home_btn)
        self.mainLayout.addWidget(self.back_btn)
        
        self.setLayout(self.mainLayout)
        

    def on_click_view_btn(self):
        filter_input = self.input_label.text()
        
        
        
        filter_choice = self.filter.currentText()
        
        record = database.extract_filter_records(filter_input,filter_choice)
        
        if len(record)==0:
            QMessageBox.information(self,"Alert","No Record Found!!!!")
            self.input_label.setText("")
        
        if self.m.scrollArea!=None:
            self.m.mainLayout.removeWidget(self.m.scrollArea)
            self.m.scrollArea.deleteLater()
            self.m.scrollArea = None

        if self.m.descScrollArea!=None:
            self.m.mainLayout.removeWidget(self.m.descScrollArea)
            self.m.descScrollArea.deleteLater()
            self.m.descScrollArea = None

        self.m.set_scroll_area(record)
        
        
        
        
        
    def on_change_choice_btn(self):
        
        if self.filter.currentText()=="trip_date":
            self.input_label.setPlaceholderText("YYYY-MM-DD")
            self.input_label.setCompleter(QCompleter([""]))
        else:
            self.input_label.setPlaceholderText("Enter "+self.filter.currentText())
            my_completer = QCompleter(database.get_list(self.filter.currentText()))
            my_completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.input_label.setCompleter(my_completer)










class record_view(QWidget):
    def __init__(self,m,record):
        super().__init__(m)
        self.top = m
        self.record = record
        self.mainLayout = QVBoxLayout()
        
        self.mainLayout.addWidget(self.header_row())
        for i in self.record:
            self.mainLayout.addWidget(entry_row(self,self.top,i))
        
        
        self.setLayout(self.mainLayout)
        
        
    def header_row(self):
        self.title = [
                    "ID","Vehicle No.","Trip Date","Material","Loading Place","Loading Machine","Unloading Place","Unloading Site",
                        
                    "Purchase Quantity","Purchase Rate","Amount Purchase","GST Bill Amount","GST Bill Number","Total Amount Purchase",
                      
                    "Sale Quantity","Sale Price","Amount Sale","Discount","Total Amount Sale",
                    
                    "Labour","Dalal Commision","Driver Commision","Toll tax","CNG/Diesel 1","CNG/Diesel 2","Police","Tyre Fitting/Puncture",
                    "Air/Grease/Filter","Others","Remarks","Total Expense Amount",
                    
                    "Work Type","Workshop/Dealer",
                    "Mechanic Name 1","Labour Charge 1","Payment Status 1",
                    "Mechanic Name 2","Labour Charge 2","Payment Status 2",
                    "Mechanic Name 3","Labour Charge 3","Payment Status 3","Spare Parts Dealer",
                    "Spare Parts Cost","Spare Parts Cost Status","GST SparePart","GST Labour","Remarks","Amount Paid By Driver","Amount Paid By Owner",
                    "Amount Unpaid",
                    
                    "Driver Name","Royality","Payment Deposit","Balance Forwarded","Balance Of Stock","In Hand Cash",
                    "Total Expense Paid By Driver","Total Profit Of Trip","Royality Given For Next Trip","Balance Forward For Next Trip"
                    ]
        header = entry_row(self,self.top,self.title)
        header.setFont(QFont("aerial",13,50,False))
        return header
    


class entry_row(QWidget):
    def __init__(self,m,top,r):
        super().__init__(m)
        self.r=r
        self.top = top
        
        self.mainLayout = QHBoxLayout()
        if not (r[0]=="ID"):
        	self.mousePressEvent = self.testlink
        for i in r:
            labelobg=QLabel(str(i),self)

            labelobg.setFixedWidth(200)
            labelobg.setAlignment(Qt.AlignLeft)
            self.mainLayout.addWidget(labelobg)

        self.setLayout(self.mainLayout)
            
    def testlink(self,evesdsdnt):
        self.top.on_click_record_row(self.r[0])



class desc_view(QWidget):
    def __init__(self,m,id):
        super().__init__(m)
        self.top = m
        record = database.extract_id_records(id)
        print(record)
        
        title = [
                    "ID","Vehicle No.","Trip Date","Material","Loading Place","Loading Machine","Unloading Place","Unloading Site",
                        
                    "Purchase Quantity","Purchase Rate","Amount Purchase","GST Bill Amount","GST Bill Number","Total Amount Purchase",
                      
                    "Sale Quantity","Sale Price","Amount Sale","Discount","Total Amount Sale",
                    
                    "Labour","Dalal Commision","Driver Commision","Toll tax","CNG/Diesel 1","CNG/Diesel 2","Police","Tyre Fitting/Puncture",
                    "Air/Grease/Filter","Others","Remarks","Total Expense Amount",
                    
                    "Work Type","Workshop/Dealer",
                    "Mechanic Name 1","Labour Charge 1","Payment Status 1",
                    "Mechanic Name 2","Labour Charge 2","Payment Status 2",
                    "Mechanic Name 3","Labour Charge 3","Payment Status 3","Spare Parts Dealer",
                    "Spare Parts Cost","Spare Parts Cost Status","GST SparePart","GST Labour","Remarks","Amount Paid By Driver","Amount Paid By Owner",
                    "Amount Unpaid",
                    
                    "Driver Name","Royality","Payment Deposit","Balance Forwarded","Balance Of Stock","In Hand Cash",
                    "Total Expense Paid By Driver","Total Profit Of Trip","Royality Given For Next Trip","Balance Forward For Next Trip"
                    ]
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(desc_top(self,record[:3]))
        self.mainLayout.addWidget(horz(self,title[3:14],record[3:14],True,5))#5
        self.mainLayout.addWidget(horz(self,title[14:31],record[14:31],True,5))#5
        self.mainLayout.addWidget(horz(self,title[31:],record[31:],True,20))
        
        
        self.setLayout(self.mainLayout)


class desc_top(QWidget):
    def __init__(self,m,record):
        super().__init__(m)
        self.setFont(QFont("aerial",13,50,False))
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Id No : "+str(record[0])))
        self.layout.addWidget(QLabel("Vehicle No: "+record[1]))
        self.layout.addWidget(QLabel("Trip Date : "+record[2]))

        self.setLayout(self.layout)


class horz(QWidget):
    def __init__(self,m,title,record,flag,where):
        super().__init__(m)
        
        self.mainLayout = QHBoxLayout()

        if flag==True:
            self.mainLayout.addWidget(vert(self,title[:where],record[:where]))
            self.mainLayout.addWidget(vert(self,title[where:],record[where:]))

        else:self.mainLayout.addWidget(vert(self,title,record))

        self.setLayout(self.mainLayout)


class vert(QWidget):
    def __init__(self,m,title,record):
        super().__init__(m)

        self.setFont(QFont("aerial",10,5,False))
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(10)
        
        for i in range(len(title)):
            row = QLabel(title[i]+" : "+str(record[i]))
            row.setFixedWidth(400)
            self.mainLayout.addWidget(row)

        self.mainLayout.insertStretch( -1, 1 )

        self.setLayout(self.mainLayout)

