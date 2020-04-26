# INTEGER TEXT NUMERIC REAL
import sqlite3


def init_db():
    conn = sqlite3.connect('databasev1.db')
    print("Opened database successfully")   

    with conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS COMPANY 
            (ID INTEGER PRIMARY KEY     AUTOINCREMENT,

            vehicle_no  TEXT    NOT NULL,
            trip_date  TEXT    NOT NULL,
            material  TEXT    NOT NULL,
            loading_place TEXT    NOT NULL,            
            loading_machine TEXT    NOT NULL,
            unloading_place TEXT    NOT NULL,
            unloading_site TEXT    NOT NULL,

            purchase_quantity REAL    NOT NULL,
            purchase_rate REAL    NOT NULL,
            amount_purchase REAL    NOT NULL,
            gst_bill_amount REAL    NOT NULL,
            gst_bill_number TEXT    NOT NULL,
            total_amount_purchase REAL    NOT NULL,

            sale_quantity REAL    NOT NULL,
            sale_price REAL    NOT NULL,
            amount_sale  REAL    NOT NULL,
            discount REAL    NOT NULL,
            total_amount_sale REAL    NOT NULL,

            labour REAL    NOT NULL,
            dalal_commision REAL    NOT NULL,
            driver_commision REAL    NOT NULL,
            toll_tax REAL    NOT NULL,
            cng_diesel_1 REAL    NOT NULL,
            cng_diesel_2 REAL    NOT NULL,
            police REAL    NOT NULL,
            tyre_fitting_puncture REAL    NOT NULL,
            air_grease_filter REAL    NOT NULL,
            others REAL    NOT NULL,
            expense_remarks TEXT    NOT NULL,
            total_expense_amount REAL    NOT NULL,
            
            work_type TEXT    NOT NULL,
            workshop_dealer TEXT    NOT NULL,
            mechanic_name_1 TEXT    NOT NULL,
            labour_charge_1 REAL    NOT NULL,
            payment_status_1 TEXT    NOT NULL,
            mechanic_name_2 TEXT    NOT NULL,
            labour_charge_2 REAL    NOT NULL,
            payment_status_2 TEXT    NOT NULL,
            mechanic_name_3 TEXT    NOT NULL,
            labour_charge_3 REAL    NOT NULL,
            payment_status_3 TEXT    NOT NULL,
            spare_parts_dealer TEXT    NOT NULL,
            spare_parts_cost REAL    NOT NULL,
            spare_parts_cost_status TEXT    NOT NULL,
            gst_spare_part TEXT    NOT NULL,
            gst_labour TEXT    NOT NULL,
            breakdown_remarks TEXT    NOT NULL,
            breakdown_amount_paid_by_driver REAL    NOT NULL,
            breakdown_amount_paid_by_owner REAL    NOT NULL,
            breakdown_amount_unpaid REAL    NOT NULL,

            driver_name TEXT    NOT NULL,
            royality REAL    NOT NULL,
            payment_deposit_by_driver REAL    NOT NULL,
            balance_forward_in_driver_account REAL    NOT NULL,
            balance_of_stock REAL    NOT NULL,
            in_hand_cash REAL    NOT NULL,
            total_expense_paid_by_driver REAL    NOT NULL,
            total_profit_of_trip REAL    NOT NULL,
            royality_given_for_next_trip REAL    NOT NULL,
            balance_forward_for_next_trip REAL    NOT NULL
            );''')
        

        print("Table created successfully")
	    




def submit_data(form_data):
	conn = sqlite3.connect('databasev1.db')
	print("hello form database")
	print(form_data)

	with conn:
		cur = conn.cursor()
		cur.execute('''INSERT INTO COMPANY(
            vehicle_no,trip_date,material ,loading_place,loading_machine,unloading_place,unloading_site,
	        
            purchase_quantity,purchase_rate,amount_purchase,gst_bill_amount,gst_bill_number,total_amount_purchase,

            sale_quantity,sale_price,amount_sale,discount,total_amount_sale,
	        
            labour,dalal_commision,driver_commision,toll_tax,cng_diesel_1,cng_diesel_2,police,tyre_fitting_puncture,air_grease_filter,
            others,expense_remarks,total_expense_amount,

            work_type,workshop_dealer,
            mechanic_name_1,labour_charge_1,payment_status_1,mechanic_name_2,labour_charge_2,payment_status_2,mechanic_name_3,labour_charge_3,payment_status_3,
            spare_parts_dealer,spare_parts_cost,spare_parts_cost_status,
	        gst_spare_part,gst_labour,breakdown_remarks, breakdown_amount_paid_by_driver,breakdown_amount_paid_by_owner,
            breakdown_amount_unpaid,

            driver_name,royality,payment_deposit_by_driver,
            balance_forward_in_driver_account, balance_of_stock ,in_hand_cash, total_expense_paid_by_driver,
            total_profit_of_trip, royality_given_for_next_trip, balance_forward_for_next_trip

            )
	        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',form_data)

		conn.commit()
		


def extract_trip_no(vehicle_no,cur_date):
	conn = sqlite3.connect('databasev1.db')
	cur_date=cur_date[:8] + "__"

	with conn:
		cur = conn.cursor()
		r = cur.execute('''select count(id) from company where vehicle_no=? and
                                trip_date like ? ''',(vehicle_no,cur_date)).fetchall()
	
		for i in r:
			trips=i[0]
		print(cur_date)

		return str(trips+1)

def get_list(t):
	conn = sqlite3.connect('databasev1.db')
	

	with conn:
		cur = conn.cursor()
		res = []
		
		r = cur.execute('''select distinct %s from company '''%t).fetchall()
		
	
		for i in r:
			res.append(i[0])
	

		return res

def extract_records():
    conn = sqlite3.connect('databasev1.db')


    with conn:
        cur = conn.cursor()
        res = []

        r = cur.execute("select * from company ").fetchall()

        for i in r:
            res.append(i)

        return (res)

def extract_filter_records(col_val,col_name):
    conn = sqlite3.connect('databasev1.db')
    col_val +="%"

    with conn:
        cur = conn.cursor()
        res = []
        
        r = cur.execute('''select * from company where %s like ? '''%col_name,(col_val,)).fetchall()        

        for i in r:
            res.append(i)

        return (res)
    
def extract_id_records(id):
    conn = sqlite3.connect('databasev1.db')

    with conn:
        cur = conn.cursor()
        res = []
        
        r = cur.execute('''SELECT * from company where ID = ? ''',(id,)).fetchone()        

        for i in r:
            res.append(i)

        return (res)


def delete_last_record():
    conn = sqlite3.connect('databasev1.db')

    with conn:
        cur = conn.cursor()
        cur.execute('''DELETE from company where id=(select max(id) from company)''')
        conn.commit()


def get_previous_forwarded_balance(vehicle_no):
    conn = sqlite3.connect('databasev1.db')
    

    with conn:
        cur = conn.cursor()
        r = cur.execute('''SELECT balance_forward_for_next_trip from company 
                            where id = (select max(id) from company where vehicle_no=?) 
                        ''',(vehicle_no,)).fetchall()
        trips = 0
        for i in r:
            trips=i[0]
        

        return str(trips)



def get_total_profit_of_day(date):
    conn = sqlite3.connect('databasev1.db')
    
    print(date)
    with conn:
        cur = conn.cursor()
        r = cur.execute('''SELECT sum(total_profit_of_trip) from company 
                            where trip_date like ? 
                        ''',(date,)).fetchall()

        for i in r:
            trips=i[0]

        return str(trips)

def get_total_profit_of_day_details(date):
    conn = sqlite3.connect('databasev1.db')
    
    print(date)
    with conn:
        cur = conn.cursor()
        r = cur.execute('''SELECT vehicle_no,sum(total_profit_of_trip) from COMPANY
                            where trip_date like ?
                            group by vehicle_no; 
                        ''',(date,)).fetchall()
        res = []
        for i in r:
            res.append(i)

        return res

def get_total_profit_of_per_day_details(date):
    conn = sqlite3.connect('databasev1.db')
    
    print("from db",date)
    with conn:
        cur = conn.cursor()
        r = cur.execute('''SELECT trip_date,sum(total_profit_of_trip) from COMPANY
                            where trip_date like ?
                            group by trip_date; 
                        ''',(date,)).fetchall()
        res = []
        for i in r:
            res.append(i)

        return res



def get_total_profit_of_per_day_vehicle_details(date,vehicle_no):
    conn = sqlite3.connect('databasev1.db')
    
    print("from db",date)
    with conn:
        cur = conn.cursor()
        r = cur.execute('''SELECT trip_date,sum(total_profit_of_trip) from COMPANY
                            where trip_date like ? and vehicle_no = ?
                            group by trip_date; 
                        ''',(date,vehicle_no,)).fetchall()
        res = []
        for i in r:
            res.append(i)

        return res