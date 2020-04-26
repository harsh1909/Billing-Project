from PyQt5.QtWidgets import *
import page2,page3,page4
from PyQt5.QtCore import Qt
import database

class home_page(QWidget):
    def __init__(self,m):
        super().__init__(m)
        database.init_db()
        self.m=m
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        #self.setFixedWidth(200) #to fix width of widget
        
        self.add_btn = QPushButton("Add",self)
        self.add_btn.clicked.connect(self.on_click_add)
        self.add_btn.setAutoDefault(True)
        self.layout.addWidget(self.add_btn)

        self.view_btn = QPushButton("View",self)
        self.view_btn.clicked.connect(self.on_click_view)
        self.layout.addWidget(self.view_btn)

        self.delete_btn = QPushButton("Delete",self)
        self.delete_btn.clicked.connect(self.on_click_delete)
        self.layout.addWidget(self.delete_btn)

        self.profit_btn = QPushButton("Profit",self)
        self.profit_btn.clicked.connect(self.on_click_profit)
        self.layout.addWidget(self.profit_btn)


        self.setLayout(self.layout)
        

    def on_click_add(self):
        print("heello add")

        vehicle_list=database.get_list("vehicle_no")
        vehicle_list.insert(0,"")
        self.vehicle_no = (QInputDialog.getItem(self,"Input","Enter Vehicle No :",vehicle_list))[0].upper()
        if len(self.vehicle_no)!=0:
            self.m.setWindowTitle("Add Entry")
            self.m.setCentralWidget(page2.page_add(self.m,self.vehicle_no))

    def on_click_view(self):
        print("hello view")
        self.m.setWindowTitle("View Entry")
        self.m.setCentralWidget(page3.page_view(self.m))

    def on_click_delete(self):
        
        ques = QMessageBox.question(self,"Alert","Delete Previous Record ?",QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if ques==QMessageBox.Yes:                                                                     #last argument is default highlighted option     
            database.delete_last_record()
            QMessageBox.information(self,"Success","Record Deleted")


    def on_click_profit(self):
        print("hello profit")
        self.m.setWindowTitle("View Profit")
        self.m.setCentralWidget(page4.page_profit(self.m))
