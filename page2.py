from contextlib import suppress
from PyQt5.QtWidgets import *
import page1 ,database
from PyQt5.QtCore import QDate, QTime,Qt
from PyQt5.QtGui import QFont ,QDoubleValidator



class page_add(QWidget):


    def __init__(self,m,vehicle_no):
        super().__init__(m)
        self.m  = m
        self.vehicle_no=vehicle_no
        
        self.layout = QVBoxLayout(self)

        self.top = top(self,self.vehicle_no)
        
        self.scrollArea = QScrollArea(self)
        self.scrollAreaWidget = my_widget(self,self.m,self.vehicle_no)
        #self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1112, 932))
        self.scrollArea.setWidget(self.scrollAreaWidget)
        
        self.layout.addWidget(self.top)
        self.layout.addWidget(self.scrollArea)
        
        self.setLayout(self.layout)

class top(QWidget):


    def __init__(self,m,vehicle_no):
        super().__init__(m)
        self.setFont(QFont("aerial",13,50,False))
        self.layout = QHBoxLayout()

        self.vehicle_no = vehicle_no
        
            
        self.vehicle_no_label = QLabel("Vehicle No: "+self.vehicle_no) 
        self.vehicle_no_label.setAlignment(Qt.AlignLeft)

        self.trip_no = QLabel("Trip No : "+database.extract_trip_no(self.vehicle_no,QDate.currentDate().toString(Qt.ISODate)))
        self.trip_no.setAlignment(Qt.AlignCenter)
        
        self.time_date =QLabel(QTime.currentTime().toString(Qt.DefaultLocaleLongDate)+"  "+ QDate.currentDate().toString(Qt.ISODate))
        self.time_date.setAlignment(Qt.AlignRight)

        self.layout.addWidget(self.vehicle_no_label)
        self.layout.addWidget(self.trip_no)
        self.layout.addWidget(self.time_date)

        self.setLayout(self.layout)



class my_widget(QWidget):


    def __init__(self,m,main,vehicle_no):
        super().__init__(m)

        self.setFixedWidth(500)
        self.m  = main
        self.vehicle_no=vehicle_no
        

        self.trip_details = QGroupBox("Trip Details")
        self.purchase_details = QGroupBox("Purchase Details")
        self.sale_details = QGroupBox("Sale Details")
        self.expense_details = QGroupBox("Trip Expense")
        self.breakdown_details = QGroupBox("Vehicle Breakdown Details")
        self.driver_details = QGroupBox("Driver Details")

        self.layout_trip_details = QFormLayout()
        self.layout_purchase_details = QFormLayout()
        self.layout_sale_details = QFormLayout()
        self.layout_expense_details = QFormLayout()
        self.layout_breakdown_details = QFormLayout()
        self.layout_driver_details = QFormLayout()
        
        self.define_form()

        self.trip_details.setLayout(self.layout_trip_details)
        self.purchase_details.setLayout(self.layout_purchase_details)
        self.sale_details.setLayout(self.layout_sale_details)
        self.expense_details.setLayout(self.layout_expense_details)
        self.breakdown_details.setLayout(self.layout_breakdown_details)
        self.driver_details.setLayout(self.layout_driver_details)
        

        self.submit_btn= QPushButton("Submit",self)
        self.submit_btn.clicked.connect(self.on_click_submit)
        

        self.home_btn= QPushButton("Home",self)
        self.home_btn.clicked.connect(self.on_click_home)
        
        self.mainLayout = QVBoxLayout()
        
        self.mainLayout.addWidget(self.trip_details)
        self.mainLayout.addWidget(self.purchase_details)
        self.mainLayout.addWidget(self.sale_details)
        self.mainLayout.addWidget(self.expense_details)
        self.mainLayout.addWidget(self.breakdown_details)
        self.mainLayout.addWidget(self.driver_details)

        self.mainLayout.addWidget(self.submit_btn)
        self.mainLayout.addWidget(self.home_btn)


        
        self.setLayout(self.mainLayout)


    
    def on_click_submit(self):
        try:
            self.get_form_data()
            self.clear()
            print(self.form_data)
            database.submit_data(self.form_data)
            QMessageBox.information(self,"Success","Record Created")
            self.on_click_home()

        except ValueError:
            QMessageBox.information(self,"ValueError","Empty Field")

    def on_click_home(self):
            print("go to home")
            
            self.m.setCentralWidget(page1.home_page(self.m))
            self.m.setWindowTitle("Home")



    def compute_amount_purchase(self):
    	res = float(self.purchase_quantity.text())*float(self.purchase_rate.text())
    	self.amount_purchase.setText(str(res))
    	
    def compute_total_amount_purchase(self):
    	res = float(self.amount_purchase.text()) + float(self.gst_bill_amount.text())
    	self.total_amount_purchase.setText(str(res))

    def compute_amount_sale(self):
    	res = float(self.sale_quantity.text())*float(self.sale_price.text())
    	self.amount_sale.setText(str(res))

    def compute_total_amount_sale(self):
    	res = float(self.amount_sale.text()) - float(self.discount.text())
    	self.total_amount_sale.setText(str(res))     

    def compute_total_expense_amount(self):
    	res = float(self.cng_diesel_1.text()) + float(self.cng_diesel_2.text()) + float(self.labour.text()) + float(self.dalal_commision.text()) + float(self.driver_commision.text()) + float(self.police.text()) + float(self.toll_tax.text()) + float(self.tyre_fitting_puncture.text()) + float(self.air_grease_filter.text()) + float(self.others.text())
    	
    	self.total_expense_amount.setText(str(res))     

    def compute_balance_of_stock(self):
    	res = float(self.royality.text()) + float(self.balance_forward_in_driver_account.text()) + float(self.total_amount_sale.text()) 

    	self.balance_of_stock.setText(str(res))

    def compute_in_hand_cash(self):
    	res = float(self.balance_of_stock.text()) - float(self.payment_deposit_by_driver.text()) -  float(self.total_expense_paid_by_driver.text())

    	self.in_hand_cash.setText(str(res))

    def compute_total_expense_paid_by_driver(self):
    	res = float(self.total_amount_purchase.text()) + float(self.total_expense_amount.text()) + float(self.breakdown_amount_paid_by_driver.text()) 

    	self.total_expense_paid_by_driver.setText(str(res))
    	self.compute_total_profit_of_trip()

    def compute_total_profit_of_trip(self):
    	res = float(self.total_amount_sale.text()) - float(self.total_expense_paid_by_driver.text()) 

    	self.total_profit_of_trip.setText(str(res))     

    def compute_balance_forward_for_next_trip(self):
    	res = float(self.in_hand_cash.text()) + float(self.royality_given_for_next_trip.text()) 

    	self.balance_forward_for_next_trip.setText(str(res))     

    def get_previous_balance_forward_for_next_trip(self):
        #ques = QMessageBox.question(self,"Alert","Get Previous Balance Forward For Next Trip ?",QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        #if ques==QMessageBox.Yes:
        return database.get_previous_forwarded_balance(self.vehicle_no)
        #return "0"


    def compute_breakdown_amount_paid_by_driver(self):
    	res = 0
    	for i in range(self.no_of_repair):
    		if self.payment_status_list[i].currentText()=="Paid By Driver":
    			res += float(self.labour_charge_list[i].text())

    	if self.spare_parts_cost_status.currentText()=="Paid By Driver":
    		res += float(self.spare_parts_cost.text())

    	self.breakdown_amount_paid_by_driver.setText(str(res))
    	self.compute_total_expense_paid_by_driver()

    def compute_breakdown_amount_paid_by_owner(self):
    	res = 0
    	for i in range(self.no_of_repair):
    		if self.payment_status_list[i].currentText()=="Paid By Owner":
    			res += float(self.labour_charge_list[i].text())

    	if self.spare_parts_cost_status.currentText()=="Paid By Owner":
    		res += float(self.spare_parts_cost.text())

    	self.breakdown_amount_paid_by_owner.setText(str(res))

    def compute_breakdown_amount_unpaid(self):
    	res = 0
    	for i in range(self.no_of_repair):
    		if self.payment_status_list[i].currentText()=="Unpaid":
    			res += float(self.labour_charge_list[i].text())

    	if self.spare_parts_cost_status.currentText()=="Unpaid":
    		res += float(self.spare_parts_cost.text())

    	self.breakdown_amount_unpaid.setText(str(res))

    def set_slots(self):
        #driver details
        self.royality.editingFinished.connect(self.update_compute)
        self.payment_deposit_by_driver.editingFinished.connect(self.update_compute)
        self.royality_given_for_next_trip.editingFinished.connect(self.update_compute)
        
        #sale details
        self.sale_quantity.editingFinished.connect(self.update_compute)
        self.sale_price.editingFinished.connect(self.update_compute)
        self.discount.editingFinished.connect(self.update_compute)
        
        #purchase details
        self.purchase_quantity.editingFinished.connect(self.update_compute)
        self.purchase_rate.editingFinished.connect(self.update_compute)
        self.gst_bill_amount.editingFinished.connect(self.update_compute)
        
        #expenses details
        self.labour.editingFinished.connect(self.update_compute)
        self.dalal_commision.editingFinished.connect(self.update_compute)
        self.driver_commision.editingFinished.connect(self.update_compute)
        self.toll_tax.editingFinished.connect(self.update_compute)
        self.cng_diesel_1.editingFinished.connect(self.update_compute)
        self.cng_diesel_2.editingFinished.connect(self.update_compute)
        self.police.editingFinished.connect(self.update_compute)
        self.tyre_fitting_puncture.editingFinished.connect(self.update_compute)
        self.air_grease_filter.editingFinished.connect(self.update_compute)
        self.others.editingFinished.connect(self.update_compute)

        #vehicle breakdown details
                
        self.labour_charge_list[0].editingFinished.connect(self.update_compute)
        self.payment_status_list[0].currentIndexChanged.connect(self.update_compute)

        self.labour_charge_list[1].editingFinished.connect(self.update_compute)
        self.payment_status_list[1].currentIndexChanged.connect(self.update_compute)
        
        self.labour_charge_list[2].editingFinished.connect(self.update_compute)
        self.payment_status_list[2].currentIndexChanged.connect(self.update_compute)
        
        self.spare_parts_cost.editingFinished.connect(self.update_compute)
        self.spare_parts_cost_status.currentIndexChanged.connect(self.update_compute)
        
        

    def update_compute(self):
        
        with suppress(ValueError):
            self.compute_amount_purchase()
        with suppress(ValueError):
            self.compute_total_amount_purchase()
        with suppress(ValueError):
            self.compute_amount_sale()
        with suppress(ValueError):
            self.compute_total_amount_sale()
        with suppress(ValueError):
            self.compute_total_expense_amount()
        with suppress(ValueError):
            self.compute_balance_of_stock()
        with suppress(ValueError):
            self.compute_in_hand_cash()
        with suppress(ValueError):
            self.compute_total_expense_paid_by_driver()
        with suppress(ValueError):
            self.compute_total_profit_of_trip()
        with suppress(ValueError):
            self.compute_balance_forward_for_next_trip()
        with suppress(ValueError):
            self.get_previous_balance_forward_for_next_trip()
        with suppress(ValueError):
            self.compute_breakdown_amount_paid_by_driver()
        with suppress(ValueError):
            self.compute_breakdown_amount_paid_by_owner()
        with suppress(ValueError):
            self.compute_breakdown_amount_unpaid()



    def define_form(self):

        #self.vehicle_no.
        #self.no_of_trip
        self.date = QDate.currentDate().toString(Qt.ISODate)
        
        #lis = ["alpha","beta","alphaman","gamma"]
        #QCompleter(database.get_list(""))
        #comp.setCaseSensitivity(Qt.CaseInsensitive)
        #.setCompleter(QCompleter(database.get_list("")))

        #trip details
        self.material = QLineEdit()
        self.material.setCompleter(QCompleter(database.get_list("material")))
        self.loading_place = QLineEdit()
        self.loading_place.setCompleter(QCompleter(database.get_list("loading_place")))
        self.loading_machine = QLineEdit()
        self.loading_machine.setCompleter(QCompleter(database.get_list("loading_machine")))
        self.unloading_place = QLineEdit()
        self.unloading_place.setCompleter(QCompleter(database.get_list("unloading_place")))
        self.unloading_site = QLineEdit()
        self.unloading_site.setCompleter(QCompleter(database.get_list("unloading_site")))


        #purchase details
        self.purchase_quantity = QLineEdit()
        self.purchase_rate = QLineEdit()
        self.amount_purchase = QLabel()
        self.gst_bill_amount = QLineEdit()
        self.gst_bill_number = QLineEdit()
        self.total_amount_purchase = QLabel()

        #self.total_amount_purchase.mousePressEvent = self.testlink
        
        #sale details
        self.sale_quantity = QLineEdit()
        self.sale_price = QLineEdit()
        self.amount_sale = QLabel() 
        self.discount = QLineEdit()
        self.total_amount_sale = QLabel()


        #expenses details

        self.labour = QLineEdit()
        self.dalal_commision = QLineEdit()
        self.driver_commision = QLineEdit()
        self.toll_tax = QLineEdit()        
        self.cng_diesel_1 = QLineEdit()
        self.cng_diesel_2 = QLineEdit()
        self.police = QLineEdit()
        self.tyre_fitting_puncture = QLineEdit()
        self.air_grease_filter = QLineEdit()
        self.others = QLineEdit()
        self.expense_remarks = QLineEdit()
        self.total_expense_amount = QLabel()
        
        #vehicle breakdown details
        self.work_type = QLineEdit()
        self.work_type.setCompleter(QCompleter(database.get_list("work_type")))
        self.workshop_dealer = QLineEdit()
        self.workshop_dealer.setCompleter(QCompleter(database.get_list("workshop_dealer")))        
        

        mechanic_name_completer = QCompleter(database.get_list("mechanic_name_1")+database.get_list("mechanic_name_2")+database.get_list("mechanic_name_3"))
        status = ["","Paid By Driver","Paid By Owner","Unpaid"]

        self.no_of_repair = 3 #(QInputDialog.getInt(self,"Input","Enter No Of Breakdown Repairs :"))[0]
        self.mechanic_name_list = [0]*self.no_of_repair
        self.labour_charge_list = [0]*self.no_of_repair
        self.payment_status_list = [0]*self.no_of_repair
        
        for i in range(self.no_of_repair):
        	#self.mechanic_name_list[i]
        	#self.labour_charge_list[i]
        	#self.payment_status_list[i]
        
        	self.mechanic_name_list[i] = QLineEdit()
        	self.mechanic_name_list[i].setCompleter(mechanic_name_completer)
        	self.labour_charge_list[i] = QLineEdit()
        	self.labour_charge_list[i].setValidator(QDoubleValidator())
        	self.payment_status_list[i] = QComboBox()
        	self.payment_status_list[i].addItems(status)	


        self.spare_parts_dealer = QLineEdit()
        self.spare_parts_dealer.setCompleter(QCompleter(database.get_list("spare_parts_dealer")))
        self.spare_parts_cost = QLineEdit()
        self.spare_parts_cost_status = QComboBox()
        self.spare_parts_cost_status.addItems(status)        

        self.gst_spare_part = QLineEdit()
        self.gst_labour = QLineEdit()
        self.breakdown_remarks = QLineEdit()
        self.breakdown_amount_paid_by_driver = QLabel()
        self.breakdown_amount_paid_by_owner = QLabel()
        self.breakdown_amount_unpaid = QLabel()

        #driver details
        self.driver_name = QLineEdit()
        self.driver_name.setCompleter(QCompleter(database.get_list("driver_name")))
        self.royality = QLineEdit()
        self.payment_deposit_by_driver = QLineEdit()
        self.balance_forward_in_driver_account = QLabel(self.get_previous_balance_forward_for_next_trip())


        self.balance_of_stock = QLabel()
        self.in_hand_cash = QLabel()
        self.total_expense_paid_by_driver = QLabel()
        self.total_profit_of_trip = QLabel()
        self.royality_given_for_next_trip = QLineEdit()
        self.balance_forward_for_next_trip = QLabel()

        self.set_slots()
        ##signals self..editingFinished.connect(self.compute_) .editingFinished.connect(self.update_compute)

        # self.purchase_rate.editingFinished.connect(self.compute_amount_purchase)
        # self.gst_bill_amount.editingFinished.connect(self.compute_total_amount_purchase)
        # self.sale_price.editingFinished.connect(self.compute_amount_sale)
        # self.discount.editingFinished.connect(self.compute_total_amount_sale)
        # self.others.editingFinished.connect(self.compute_total_expense_amount)

        # self.breakdown_remarks.editingFinished.connect(self.compute_breakdown_amount_paid_by_driver)
        # self.breakdown_remarks.editingFinished.connect(self.compute_breakdown_amount_paid_by_owner)
        # self.breakdown_remarks.editingFinished.connect(self.compute_breakdown_amount_unpaid)

        # self.royality.editingFinished.connect(self.compute_balance_of_stock)
        # self.payment_deposit_by_driver.editingFinished.connect(self.compute_in_hand_cash)
        # self.royality_given_for_next_trip.editingFinished.connect(self.compute_balance_forward_for_next_trip)




        ##validators

        #purchase details
        self.purchase_quantity.setValidator(QDoubleValidator())
        self.purchase_rate.setValidator(QDoubleValidator())
        self.gst_bill_amount.setValidator(QDoubleValidator())


        #sale details
        self.sale_quantity.setValidator(QDoubleValidator())
        self.sale_price.setValidator(QDoubleValidator())
        self.discount.setValidator(QDoubleValidator())


        #expenses details
        self.labour.setValidator(QDoubleValidator())
        self.dalal_commision.setValidator(QDoubleValidator())
        self.driver_commision.setValidator(QDoubleValidator())
        self.toll_tax.setValidator(QDoubleValidator())
        self.cng_diesel_1.setValidator(QDoubleValidator())
        self.cng_diesel_2.setValidator(QDoubleValidator())
        self.police.setValidator(QDoubleValidator())
        self.tyre_fitting_puncture.setValidator(QDoubleValidator())
        self.air_grease_filter.setValidator(QDoubleValidator())
        self.others.setValidator(QDoubleValidator())
        
        
        #vehicle breakdown details
        self.spare_parts_cost.setValidator(QDoubleValidator())

        #driver details
        self.royality.setValidator(QDoubleValidator())
        self.payment_deposit_by_driver.setValidator(QDoubleValidator())
        self.royality_given_for_next_trip.setValidator(QDoubleValidator())



        width = 200
        
        #add to layout
        #trip details
        label1 = QLabel(" Material:")
        label1.setFixedWidth(width)
        self.layout_trip_details.addRow(label1, self.material)
        self.layout_trip_details.addRow(QLabel(" Loading Place:"), self.loading_place)
        self.layout_trip_details.addRow(QLabel(" Loading Machine:"), self.loading_machine)
        self.layout_trip_details.addRow(QLabel(" Unloading Place:"), self.unloading_place)
        self.layout_trip_details.addRow(QLabel(" Unloading Site:"), self.unloading_site)

        #purchase details
        label2 = QLabel(" Purchase Quantity:")
        label2.setFixedWidth(width)
        self.layout_purchase_details.addRow(label2, self.purchase_quantity)
        self.layout_purchase_details.addRow(QLabel(" Purchase Rate:"), self.purchase_rate)
        self.layout_purchase_details.addRow(QLabel(" Amount Purchase:"), self.amount_purchase)		#purchaseQuanty * Purchase rate
        self.layout_purchase_details.addRow(QLabel(" GST Bill Amount:"), self.gst_bill_amount)
        self.layout_purchase_details.addRow(QLabel(" GST Bill No:"), self.gst_bill_number)
        self.layout_purchase_details.addRow(QLabel(" Total Amount Purchase:"), self.total_amount_purchase)		#amount purchase + gst bill amount

        
        #sale details
        label3 = QLabel(" Sale Quantity:")
        label3.setFixedWidth(width)
        self.layout_sale_details.addRow(label3, self.sale_quantity)
        self.layout_sale_details.addRow(QLabel(" Sale Price:"), self.sale_price)	
        self.layout_sale_details.addRow(QLabel(" Amount Sale:"), self.amount_sale)	#sale_quanity*sale_price
        self.layout_sale_details.addRow(QLabel(" Discount"), self.discount)
        self.layout_sale_details.addRow(QLabel(" Total Amount Sale:"), self.total_amount_sale)	#amount_sale-disount

        #expenses details
        label4 = QLabel(" Labour:")
        label4.setFixedWidth(width)
        self.layout_expense_details.addRow(label4, self.labour)
        self.layout_expense_details.addRow(QLabel(" Dalal Commision:"), self.dalal_commision)
        self.layout_expense_details.addRow(QLabel(" Driver Commision:"), self.driver_commision)
        self.layout_expense_details.addRow(QLabel(" Toll Tax:"), self.toll_tax)
        self.layout_expense_details.addRow(QLabel(" CNG/Diesel 1:"), self.cng_diesel_1)
        self.layout_expense_details.addRow(QLabel(" CNG/Diesel 2:"), self.cng_diesel_2)
        self.layout_expense_details.addRow(QLabel(" Police:"), self.police)
        self.layout_expense_details.addRow(QLabel(" Tyre Fitting Puncture:"), self.tyre_fitting_puncture)
        self.layout_expense_details.addRow(QLabel(" Air Grease Filter:"), self.air_grease_filter)
        self.layout_expense_details.addRow(QLabel(" Others:"), self.others)
        self.layout_expense_details.addRow(QLabel(" Remarks:"), self.expense_remarks)
        self.layout_expense_details.addRow(QLabel(" Total Expense Amount:"), self.total_expense_amount)		#all expenses including other excluding remarks
        
        #vehicle breakdown details
        label5 = QLabel(" Work Type:")
        label5.setFixedWidth(width)
        self.layout_breakdown_details.addRow(label5, self.work_type)
        self.layout_breakdown_details.addRow(QLabel(" Workshop/Dealer:"), self.workshop_dealer)

        
        for i in range(self.no_of_repair):
        	self.layout_breakdown_details.addRow(QLabel(" Mechanic Name "+str(i+1)+":"), self.mechanic_name_list[i])
        	self.layout_breakdown_details.addRow(QLabel(" Labour Charge "+str(i+1)+":"), self.labour_charge_list[i])
        	self.layout_breakdown_details.addRow(QLabel(" Payment Status "+str(i+1)+":"), self.payment_status_list[i])
        

        self.layout_breakdown_details.addRow(QLabel(" Spare Parts Dealer:"), self.spare_parts_dealer)
        self.layout_breakdown_details.addRow(QLabel(" Spare Parts Cost:"), self.spare_parts_cost)
        self.layout_breakdown_details.addRow(QLabel(" Spare Parts Cost Status:"), self.spare_parts_cost_status)
        #spare_parts_cost_status
        self.layout_breakdown_details.addRow(QLabel(" GST Spare Part:"), self.gst_spare_part)
        self.layout_breakdown_details.addRow(QLabel(" GST Labour:"), self.gst_labour)
        self.layout_breakdown_details.addRow(QLabel(" Remarks:"), self.breakdown_remarks)
        self.layout_breakdown_details.addRow(QLabel(" Amount Paid By Driver:"), self.breakdown_amount_paid_by_driver)
        self.layout_breakdown_details.addRow(QLabel(" Amount Paid By Owner:"), self.breakdown_amount_paid_by_owner)
        self.layout_breakdown_details.addRow(QLabel(" Amount Unpaid:"), self.breakdown_amount_unpaid)


        #driver details
        label6 = QLabel(" Driver Name:")
        label6.setFixedWidth(width)
        self.layout_driver_details.addRow(label6, self.driver_name)
        self.layout_driver_details.addRow(QLabel(" Royality:"), self.royality)
        self.layout_driver_details.addRow(QLabel(" Payment Deposit:"), self.payment_deposit_by_driver)
        self.layout_driver_details.addRow(QLabel(" Balance Forwarded:"), self.balance_forward_in_driver_account)	#extacted from previous trip of same vehicle
        self.layout_driver_details.addRow(QLabel(" Balance Of Stock:"), self.balance_of_stock)	#royality + balance_forward + total_amout_sale
        self.layout_driver_details.addRow(QLabel(" In Hand Cash:"), self.in_hand_cash)			#balance of _stock - payment_deposit_by_driver
        self.layout_driver_details.addRow(QLabel(" Total Expense Paid By Driver:"), self.total_expense_paid_by_driver)	#total_amount_purchase + total_trip_expense + total_breakdown_paid_by_driver
        self.layout_driver_details.addRow(QLabel(" Total Profit Of Trip:"), self.total_profit_of_trip)	#total_ampunt_sale - total_expense_paid_by_driver
        self.layout_driver_details.addRow(QLabel(" Royality Given For Next Trip:"), self.royality_given_for_next_trip)	
        self.layout_driver_details.addRow(QLabel(" Balance Forward For Next Trip:"), self.balance_forward_for_next_trip)	#inhand_cash + Royality_given_for_next_trip




        self.clear()
        
    
    def get_form_data(self):
    	self.form_data = [  self.vehicle_no, self.date,
    	
		    	self.material.text(),                    self.loading_place.text(),            self.loading_machine.text(), 
		    	self.unloading_place.text(),             self.unloading_site.text(),

		    	float(self.purchase_quantity.text()),    float(self.purchase_rate.text()),     float(self.amount_purchase.text()),
		        float(self.gst_bill_amount.text()) ,     self.gst_bill_number.text() ,         float(self.total_amount_purchase.text()),

		    	float(self.sale_quantity.text()),        float(self.sale_price.text()),        float(self.amount_sale.text()),
		    	float(self.discount.text()),             float(self.total_amount_sale.text()),           

		    	float(self.labour.text()),               float(self.dalal_commision.text()), 
		    	float(self.driver_commision.text()),     float(self.toll_tax.text()),
		    	float(self.cng_diesel_1.text()),         float(self.cng_diesel_2.text()),      float(self.police.text()),             
		    	float(self.tyre_fitting_puncture.text()),float(self.air_grease_filter.text()), float(self.others.text()), 
		    	self.expense_remarks.text(),             float(self.total_expense_amount.text()),
		        
		        self.work_type.text(),                   self.workshop_dealer.text(),          
		        self.mechanic_name_list[0].text() , float(self.labour_charge_list[0].text()) , self.payment_status_list[0].currentText(),
		        self.mechanic_name_list[1].text() , float(self.labour_charge_list[1].text()) , self.payment_status_list[1].currentText(), 
		        self.mechanic_name_list[2].text() , float(self.labour_charge_list[2].text()) , self.payment_status_list[2].currentText(), 
		        
		        self.spare_parts_dealer.text(),
		        float(self.spare_parts_cost.text()),     self.spare_parts_cost_status.currentText(),  self.gst_spare_part.text(),           
		        self.gst_labour.text(),                  self.breakdown_remarks.text(),
		        float(self.breakdown_amount_paid_by_driver.text()) , 
		        float(self.breakdown_amount_paid_by_owner.text()), 
		        float(self.breakdown_amount_unpaid.text()),

		        self.driver_name.text(),                        float(self.royality.text()),
		    	float(self.payment_deposit_by_driver.text()),   float(self.balance_forward_in_driver_account.text()), 
		    	float(self.balance_of_stock.text()),            float(self.in_hand_cash.text()),
		    	float(self.total_expense_paid_by_driver.text()), float(self.total_profit_of_trip.text()),
		    	float(self.royality_given_for_next_trip.text()) ,float(self.balance_forward_for_next_trip.text())

        		]


    def clear(self):
    	#trip details
        self.material.setText("")
        self.loading_place.setText("")
        self.loading_machine.setText("")
        self.unloading_place.setText("")
        self.unloading_site.setText("")

        #purchase details
        self.purchase_quantity.setText("")
        self.purchase_rate.setText("")
        self.amount_purchase.setText("")
        self.gst_bill_amount.setText("")
        self.gst_bill_number.setText("")
        self.total_amount_purchase.setText("")
        
        #sale details
        self.sale_quantity.setText("")
        self.sale_price.setText("")
        self.amount_sale.setText("") 
        self.discount.setText("")
        self.total_amount_sale.setText("")

        #expenses details
        self.labour.setText("")
        self.dalal_commision.setText("")
        self.driver_commision.setText("")
        self.toll_tax.setText("")
        self.cng_diesel_1.setText("")
        self.cng_diesel_2.setText("")
        self.police.setText("")
        self.tyre_fitting_puncture.setText("")
        self.air_grease_filter.setText("")
        self.others.setText("")
        self.expense_remarks.setText("")
        self.total_expense_amount.setText("")
        
        #vehicle breakdown details
        self.work_type.setText("")
        self.workshop_dealer.setText("")
        self.spare_parts_dealer.setText("")
        self.spare_parts_cost.setText("")
        self.gst_spare_part.setText("")
        self.gst_labour.setText("")
        self.breakdown_remarks.setText("")
        self.breakdown_amount_paid_by_driver.setText("")
        self.breakdown_amount_paid_by_owner.setText("")
        self.breakdown_amount_unpaid.setText("")

        #driver details
        self.driver_name.setText("")
        self.royality.setText("")
        self.payment_deposit_by_driver.setText("")
        #self.balance_forward_in_driver_account.setText("")
        self.balance_of_stock.setText("")
        self.in_hand_cash.setText("")
        self.total_expense_paid_by_driver.setText("")
        self.total_profit_of_trip.setText("")
        self.royality_given_for_next_trip.setText("")
        self.balance_forward_for_next_trip.setText("")



    def cclear(self):
    	#trip details
        self.material.setText("dsgfsdg")
        self.loading_place.setText("fdg")
        self.unloading_place.setText("sdgfsd")
        self.loading_machine.setText("sdgdg")
        self.unloading_site.setText("sdgsdg")

        #driver details
        self.driver_name.setText("sdgsdgd")
        self.royality.setText("4560")
        self.payment_deposit_by_driver.setText("456456")
        #self.balance_forward_in_driver_account.setText("234")
        self.balance_of_stock.setText("45645")
        self.in_hand_cash.setText("23423")
        self.total_expense_paid_by_driver.setText("34534")
        self.total_profit_of_trip.setText("23454")
        self.royality_given_for_next_trip.setText("23542")
        self.balance_forward_for_next_trip.setText("1231")
        
        #sale details
        self.sale_quantity.setText("453")
        self.sale_price.setText("2432")
        self.amount_sale.setText("3243") 
        self.discount.setText("2342")        
        self.total_amount_sale.setText("1432")

        #purchase details
        self.purchase_quantity.setText("4365346")
        self.purchase_rate.setText("14324")
        self.amount_purchase.setText("436346")
        self.gst_bill_amount.setText("45745")
        self.gst_bill_number.setText("zxfdsdf")
        self.total_amount_purchase.setText("235345")

        #expenses details
        self.cng_diesel_1.setText("34564")
        self.cng_diesel_2.setText("34564")
        self.labour.setText("23453")
        self.dalal_commision.setText("23534")
        self.driver_commision.setText("23534")
        self.police.setText("34234")
        self.toll_tax.setText("234")
        self.others.setText("325")
        self.expense_remarks.setText("nil")
        self.tyre_fitting_puncture.setText("34534")
        self.air_grease_filter.setText("243534")
        self.total_expense_amount.setText("345345")
        
        
        #vehicle breakdown details
        self.work_type.setText("dfgfdg")
        
        self.spare_parts_cost.setText("34543")
        

        #self.payment_status.setText("234234")
        self.spare_parts_dealer.setText("34234")
        self.workshop_dealer.setText("dsfsdf")
        self.gst_spare_part.setText("fjfgj")
        self.gst_labour.setText("dfgdfhg")
        self.breakdown_remarks.setText("nonono")
        self.breakdown_amount_paid_by_driver.setText("32423")
        self.breakdown_amount_paid_by_owner.setText("23523")
        self.breakdown_amount_unpaid.setText("235235")
