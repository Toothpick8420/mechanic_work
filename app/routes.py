from app import app
from datetime import date
from flask import flash, redirect, render_template, request, session
import mysql.connector
# For hashing password
import hashlib
import os

# TODO:
# - Make session expiration

# Database object
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="mechanic" # Subject to change
)
cursor = db.cursor() # to interact with the database


# User login
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        userID   = request.form['userID'].strip()
        password = request.form['password']

        if len(userID) == 0:
            flash('Enter userID')
            return redirect('/login')

        try:    
            userID = int(userID)
        except ValueError:
            flash('UserID wrong input')
            return redirect('/login')


        # Check username
        cursor.execute(f'SELECT password, salt FROM LOGIN WHERE userID={userID}')
    
        accounts = cursor.fetchall()

        if len(accounts) == 0:
            flash('UserID Incorrect')
            return redirect('/login')

        # Check password
        password = str.encode(password)
        salted   = password + accounts[0][1]
        hashed   = hashlib.sha256(salted)

        # Compare passwords
        if (hashed.hexdigest() != accounts[0][0].hex()):
            flash('Password Incorrect')
            return redirect('/login')

        
        # Login was correct so move on
        return redirect('/homepage')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('create_account.html')
    
    # POST method, an attempt to create an account 
    fname  = request.form['fname'].strip()
    lname  = request.form['lname'].strip()
    userID = request.form['userID'].strip()
    email  = request.form['email'].strip()
    password = request.form['password']
    store  = request.form['storenum'].strip()

    if ' ' in fname or ' ' in lname:
        flash('Cannot have space in name')
        return redirect('create_account')

    # Make sure the userID is an int
    try:
        userID = int(userID)
    except ValueError:
        flash('userID is not an integer')
        return redirect('create_account')

    # Check if the userID is taken
    cursor.execute(f'SELECT userID FROM EMPLOYEE WHERE userID="{userID}"')
    if len(cursor.fetchall()) != 0:
        flash('userID already taken')
        return redirect('create_account')
 
    # Make sure that the password is in the lengths
    if len(password) < 10 or len(password) > 25:
        flash('Password length invalid')
        return redirect('create_account')

    # Make sure the password has all the information
    special_chars = "!\"#$%&'()*+,-./<=>?@[]^_`{|}"
    has_alpha   = False
    has_special = False
    has_upper   = False
    has_lower   = False
    has_num     = False
    for char in password:
        if char in special_chars:
            has_special = True
        elif char.isalpha():
            has_alpha = True
            if char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
        elif char.isnumeric():
                has_num = True
        
    if (not has_alpha or not has_special or 
        not has_upper or not has_lower or not has_num):
        flash('Password does not meet requirements')
        return redirect('create_account')

    # Make sure the store number is valid
    cursor.execute(f'SELECT shopNum FROM SHOP WHERE shopNum="{store}"')
    if len(cursor.fetchall()) == 0:
        flash('Invalid store number')
        return redirect('create_account')
 
    # salt and hash the password
    salt = os.urandom(10) # 10 byte salt
    password = str.encode(password) # convert the string password to bytes
    salted = password + salt # salted password
    hashed = hashlib.sha256(salted).digest() # Hash the password

    # Store the Login information
    cursor.execute(f'''
        INSERT INTO LOGIN
        VALUES ({userID}, 0x{hashed.hex()}, 0x{salt.hex()})
    ''')



    today = str(date.today())
    # Put the other information in the Employee  table
    cursor.execute(f'''
        INSERT INTO EMPLOYEE (userID, hiredate, shopNum, firstName, lastName, email)
        VALUES ({userID}, "{today}", {store}, "{fname}", "{lname}",  "{email}")
    ''')

    # Commit the changes to the database
    db.commit()

    # redirect to the login page now for  them to login
    return redirect('/login')


@app.route('/homepage')
def homepage():
    return render_template('homepage.html')


@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'GET':
        page = render_template('appointments.html')

        # Read in all appointments in the database
        cursor.execute('''
            SELECT appDate, app.custID, app.VIN, shopNum, year, make, model, appNum
            FROM APPOINTMENTS as app JOIN CAR
            WHERE app.VIN = CAR.VIN
        ''')

        results = cursor.fetchall()
        
        # Append all the appointments to the webpage we are building
        results = sorted(results)
        for app in results:
            # TODO: Instead of custID get their name from the CUSTOMER table
            appointment = f'''<ul>Appointment {app[7]:<4d}> {app[0]} | {app[1]} - {app[4]:>7} {app[5]:<20}  {app[6]: <5} {app[2]:>5}</ul>'''
            page += appointment

        return page

    elif request.method == 'POST':
        appnum = request.form['appnum']
        try:
            appnum = int(appnum)
        except ValueError:
            flash('Invalid appointment format entered to remove')
            return redirect('/appointments')

        cursor.execute(f"SELECT appNum FROM APPOINTMENTS WHERE appNum={appnum}")
        if len(cursor.fetchall()) == 0:
               print(f'Appointments: Invalid appnum {appnum} entered')
               return redirect('/appointments')

        cursor.execute(f'''
            DELETE FROM APPOINTMENTS WHERE appNum={appnum}
        ''')
        db.commit()
        return redirect('/appointments')


@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'GET':
        return render_template('add_appointment.html')

    custid = request.form['custID'].strip()
    date   = request.form['date']
    vin    = request.form['vin'].strip()
    shop   = request.form['shop'].strip()

    try:
        custid = int(custid)
        shop   = int(shop)
    except ValueError:
        flash('Non integer value entered')
        return redirect('/add_appointment')

    if ' ' in vin:
        flash('Invalid vin input')
        return redirect('/add_appointment')

    cursor.execute(f'''SELECT custID FROM CUSTOMER WHERE custID={custid}''')
    if len(cursor.fetchall()) == 0:
        flash('CustID not found, please add customer first')
        return redirect('/add_appointment')
    
    # Check if the car is in the database already
    cursor.execute(f''' SELECT VIN FROM CAR WHERE VIN="{vin}" ''')
    if len(cursor.fetchall()) == 0:
        flash('VIN not found in database, please add car')
        return redirect('/add_appointment')

    cursor.execute(f'''
        INSERT INTO APPOINTMENTS (appDate, VIN, custID, shopNum)
        VALUES ("{date}", "{vin}", {custid}, {shop})
    ''')

    db.commit()

    return redirect('/appointments')


@app.route('/suppliers', methods=['GET', 'POST'])
def suppliers():
    if request.method == 'GET':
        return render_template('suppliers.html')
    elif request.method == 'POST':
        webpage = render_template('suppliers.html')
        store   = request.form['shop'].strip()

        if len(store) == 0:
            store = 0
        else:
            try:
                store = int(store)
            except ValueError:
                print('SuppliersError: Invalid store number passed')
                return redirect('/suppliers')

        if store == 0:
            cursor.execute('SELECT * FROM SUPPLIER')
        else:
            cursor.execute(f'''
                SELECT * FROM SUPPLIER WHERE shopNum={store}
            ''')

        results = cursor.fetchall()

        if store == 0:
            webpage += f"Suppliers for all stores<br>"
        else:
            webpage += f"Suppliers for store {store}:<br>"

        if len(results) == 0:
            webpage += "No Results Found<br>"

        for supplier in results:
            webpage += f'''
                <ul>Supplier {supplier[0]}: {supplier[1]}, {supplier[4]} {supplier[2]} {supplier[3]}</ul>
            '''

        return webpage


@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'GET':
        return render_template('add_supplier.html')
    elif request.method == 'POST':

        phone = request.form['phone'].strip()
        store = request.form['shop']
        city = request.form['city'].strip()
        state = request.form['state'].strip()
        address = request.form['address'].strip()

        try: 
            store = int(store)
        except ValueError:
            flash('Error in store number format')
            return redirect('/suppliers')
        
        if (len(phone) != 10):
            flash('Invalid phone number')
            return redirect('/suppliers')

        cursor.execute(f'SELECT shopNum FROM SHOP WHERE shopNum={store}')

        if (len(cursor.fetchall()) == 0):
            flash('Invalid store number')
            return redirect('/suppliers')


        cursor.execute(f'''
            INSERT INTO SUPPLIER (phoneNumber, city, state, address, shopNum)
            VALUES ("{phone}", "{city}", "{state}", "{address}", {store})
        ''')

        db.commit()

        return redirect('/suppliers')


@app.route('/remove_supplier', methods=['POST'])
def remove_supplier():
    
    supplier = request.form['supplier'].strip()

    try:
        supplier = int(supplier)
    except ValueError:
        flash ('Invalid supplier num')
        return redirect('/suppliers') 

    cursor.execute(f'''
        DELETE FROM SUPPLIER WHERE supplierNum={supplier}
    ''')
    db.commit()

    return redirect('/suppliers')


@app.route('/cars', methods=['GET', 'POST'])
def cars():
    if request.method == 'GET':
        return render_template('cars.html')
    elif request.method == 'POST':          
        webpage = render_template('cars.html')
        fname = request.form['fname'].strip()
        lname = request.form['lname'].strip()
        phone = request.form['phone'].strip()

        
        if len(fname) == 0 and len(lname) == 0 and len(phone) == 0:
            cursor.execute(f'''
                SELECT custID FROM CUSTOMER
            ''')
        else:
            cursor.execute(f'''
                SELECT custID FROM CUSTOMER 
                WHERE firstName="{fname}" or lastName="{lname}" or phoneNumber="{phone}"
            ''')

        results = cursor.fetchall()
        if len(results) == 0:
            return (webpage + "No results found")

        vehicles = []
        for custid in results:
            cursor.execute(f'''
                SELECT year, make, model, vin, custID FROM CAR
                WHERE custID={custid[0]}
            ''')
            vehicles += cursor.fetchall()

        if len(vehicles) == 0:
            webpage += "No results found"

        else:   
            for vehicle in vehicles:
                webpage += f"<ul>CustID: {vehicle[4]} - {vehicle[0]} {vehicle[1]} {vehicle[2]} {vehicle[3]}</ul>"

        return webpage


@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'GET':
        return render_template('add_car.html')
    elif request.method == 'POST':

        vin = request.form['vin'].strip()
        make = request.form['make'].strip()
        model = request.form['model'].strip()
        year = request.form['year']
        custid = request.form['custid']

        try:
            year = int(year)
            custid = int(custid)
        except ValueError:
            flash('Noninteger input for integer values')
            return redirect('/add_car')

        if len(vin) <= 0 or len(vin) > 17:
            flash('Invalid vin length')
            return redirect('/add_car')

        cursor.execute(f'SELECT custID FROM CUSTOMER WHERE custID={custid}')
        if len(cursor.fetchall()) == 0:
            flash('Invalid custID, try again or add customer')
            return redirect('/add_car')

        cursor.execute(f'''
            INSERT INTO CAR 
            VALUES ("{vin}", "{make}", "{model}", {year}, {custid})
        ''')

        db.commit()
        return redirect('/cars')


@app.route('/remove_car', methods=['POST'])
def remove_car():
    vin = request.form['vin'].strip()

    print('requestcar')

    if ' ' in vin:
        flash('Invalid vin format')
        return redirect('/cars')
    
    cursor.execute(f'''
        DELETE FROM APPOINTMENTS
        WHERE VIN="{vin}"
    ''')

    cursor.execute(f'''
        DELETE FROM CAR
        WHERE VIN="{vin}"
    ''')

    db.commit()

    return redirect('/cars')


@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'GET':
        return render_template('customers.html')
    elif request.method == 'POST': 
            # Search for customer in databse
        fname = request.form['fname'].strip()
        lname = request.form['lname'].strip()
        phone = request.form['phone'].strip()

        webpage = render_template('customers.html')

        # input validation
        if ' ' in fname or ' ' in lname or ' ' in phone:
            flash('Space in input not allowed')
            return redirect('/customers')

        if len(fname) == 0 and len(lname) == 0 and len(phone) == 0:
            cursor.execute('SELECT * FROM CUSTOMER')
        else:
            cursor.execute(f'''
                SELECT * FROM CUSTOMER
                WHERE firstName="{fname}" or lastName="{lname}" or phoneNumber="{phone}"
            ''')
        
        results = cursor.fetchall()

        if len(results) == 0:
            webpage += "No results found <br>"
        else:
            for customer in results:
                cust = f"<p>CustID:{customer[0]}<br> Name: {customer[1]} {customer[2]}<br> Phone Number:{customer[3]}<br></p>"
                cursor.execute(f'SELECT VIN FROM CAR WHERE custID={customer[0]}')
                webpage += cust
                vehicles = cursor.fetchall()
                for car in vehicles:
                    webpage += f'VIN: {car[0]}<br>'
        
        return webpage


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'GET':
        return render_template('add_customer.html')
    elif request.method == 'POST':

        fname = request.form['fname'].strip()
        lname = request.form['lname'].strip()
        phone = request.form['phone'].strip()

        # input validation
        if ' ' in fname or ' ' in lname or ' ' in phone:
            flash('Spaces in input not allowed')
            return redirect('/add_customer')

        if len(phone) != 10:
            flash('Phone number is incorrect length')
            return redirect('/add_customer')


        # Add into customer table 
        cursor.execute(f'''
            INSERT INTO CUSTOMER (firstName, lastName, phoneNumber)
            VALUES ("{fname}", "{lname}", "{phone}")
        ''')

        # Ge the custID
        cursor.execute(f'''
            SELECT * FROM CUSTOMER 
            WHERE firstName="{fname}" and lastName="{lname}" and phoneNumber="{phone}"
        ''')

        cust = cursor.fetchall()
        if len(cust) == 0:
            flash('Error during adding customer, try again...')
            return redirect('/add_customer')


        db.commit()

        return redirect('/customers')


@app.route('/repairs', methods=['GET', 'POST'])
def repairs():
    if request.method == 'GET':
        return render_template('repairs.html')
    elif request.method == 'POST':

        webpage = render_template('repairs.html')

        fname = request.form['fname'].strip()
        lname = request.form['lname'].strip()
        phone = request.form['phone'].strip()
        vin   = request.form['vin'].strip()

        if len(fname) == 0 and len(lname) == 0 and len(phone) == 0:
            cursor.execute(f'''
                SELECT custID FROM CUSTOMER 
            ''')
        else:
            cursor.execute(f'''
                SELECT custID FROM CUSTOMER 
                WHERE firstName="{fname}" or lastName="{lname}" or phoneNumber="{phone}"
            ''')

        possibleIDs = cursor.fetchall()
       
        possibleVINs = []
        for id in possibleIDs:
            cursor.execute(f'''
               SELECT VIN, custID FROM CAR WHERE custID={id[0]}
            ''')
            res = cursor.fetchall()
            if len(res) != 0:
                possibleVINs += res

        results = []
        if len(possibleIDs) == 0:
            cursor.execute(f'SELECT * FROM REPAIR WHERE VIN="{vin}"')
            results = cursor.fetchall()
        else:
            for vin in possibleVINs:
                cursor.execute(f'SELECT * FROM REPAIR WHERE VIN="{vin[0]}"')
                results += cursor.fetchall()

        if len(results) == 0:
            webpage += 'No Results Found'


        for result in results:
            webpage += f'''<p>
                Repair #{result[0]} <br>
                Assigned: {result[2]}<br>
                Vehicle: {result[1]} <br>
                In Miles: {result[3]} <br>
                Out Miles: {result[4]} <br>
            </p>'''

        return webpage


@app.route('/add_repair', methods=['GET', 'POST'])
def add_repair():
    if request.method == 'GET':
        return render_template('add_repair.html')
    elif request.method == 'POST':

        userID = request.form['userID'] 
        vin = request.form['vin'].strip()
        miles = request.form['in_miles']


        try:
            userID = int(userID)
            miles = float(miles)
        except ValueError:
            flash('Non integer value entered for TechID or milage')
            return redirect('/add_repair')

        cursor.execute(f'SELECT userID FROM EMPLOYEE WHERE userID={userID}')
        if len(cursor.fetchall()) == 0:
            flash('Invalid techID entered')
            return redirect('/add_repair')

        cursor.execute(f'SELECT VIN FROM CAR WHERE VIN="{vin}"')
        if len(cursor.fetchall()) == 0:
            flash('Car not found, please add car')
            return redirect('/add_repair')
        
        cursor.execute(f'''
            INSERT INTO REPAIR (userID, VIN, in_miles)
            VALUES ({userID}, "{vin}", {miles})
        ''')


        db.commit() 
        return redirect('/repairs')




@app.route('/update_repair', methods=['POST'])
def update_repair():
    repairNum = request.form['repairNum']
    out_miles = request.form['out_miles']

    try:
        repairNum=int(repairNum)
        out_miles=float(out_miles)
    except ValueError:
        flash('Invalid input for update repair')
        return redirect('/repairs')


    cursor.execute(f'''
        UPDATE REPAIR
        SET out_miles={out_miles}
        WHERE repairNum={repairNum}
    ''')

    db.commit()

    return redirect('/repairs')


@app.route('/get_tasks', methods=['POST'])
def get_tasks():
        
    webpage = render_template('repairs.html')
    repairNum = request.form['repairNum']

    try: 
        repairNum = int(repairNum)
    except ValueError:
        flash('Invaid repair number format to get tasks')
        return redirect('/repairs')

    cursor.execute(f'''
        SELECT * FROM TASK WHERE repairNum={repairNum}
    ''')
    results = cursor.fetchall()

    for task in results:
        webpage += f'''<p>
            {task[2]}<br>
        </p>'''

    if len(results) == 0:
        webpage += '<br>No Tasks On File Yet...'

    return webpage


@app.route('/add_task', methods=['POST'])
def add_task():
    repairNum = request.form['repairNum'].strip()
    descr     = request.form['descr'].strip()

    try:
        repairNum = int(repairNum)
    except ValueError:
        flash('Invalid repair number format to add task')
        return redirect('/add_repair')

    cursor.execute(f'SELECT repairNum FROM REPAIR where repairNum={repairNum}')
    if (len(cursor.fetchall()) == 0):
        flash('Invalid repair number, enter correct repair number and try again')
        return redirect('/add_repair')

    cursor.execute(f'''
        INSERT INTO TASK (repairNum, description)
        VALUES ({repairNum}, "{descr}")
    ''')

    db.commit()

    return redirect('/repairs')


@app.route('/invoices', methods=['GET', 'POST'])
def invoices():
    if request.method == 'GET':
        return render_template('invoices.html')
    elif request.method == 'POST':

        webpage = render_template('invoices.html')
        fname = request.form['fname'].strip()
        lname = request.form['lname'].strip()
        phone = request.form['phone'].strip()


        if len(fname) == 0 and len(lname) == 0 and len(phone) == 0:
            cursor.execute('SELECT custID FROM CUSTOMER')
        else:
            cursor.execute(f'''
                SELECT custID FROM CUSTOMER 
                WHERE firstName="{fname}" or lastName="{lname}" or phoneNumber="{phone}"
            ''')

        results = cursor.fetchall()
        if len(results) == 0:
            return (webpage + "No results found")

        invs= []
        for custID in results:
            cursor.execute(f'''
                SELECT * FROM INVOICE WHERE custID={custID[0]}
            ''')
            invs += cursor.fetchall()


        for invoice in invs:
            paid = ""
            if (invoice[6] == 0):
                paid = "No"
            else:
                paid = "Yes"

            webpage += f'''<p>
                Invoice #: {invoice[0]}<br>
                Worked on by: {invoice[1]}<br>
                VIN: {invoice[3]}<br>
                CustID: {invoice[2]}<br>
                Repair Number: {invoice[4]}<br>
                Total Cost: {invoice[5]}<br>
                Paid: {paid}<br>
            </p>'''

        return webpage


@app.route('/add_invoice', methods=['GET', 'POST'])
def add_invoice():
    if request.method == 'GET':
        return render_template('add_invoice.html')
    elif request.method == 'POST':

        userID = request.form['userID'] 
        custID = request.form['custID']
        vin = request.form['vin'].strip()
        repairNum = request.form['repairNum']
        cost = request.form['cost']

        try:
            userID = int(userID)
            custID = int(custID)
            repairNum = int(repairNum)
            cost = float(cost)
        except ValueError:
            flash('Error in entered values')
            return redirect('/add_invoice')

        cursor.execute(f'SELECT userID FROM EMPLOYEE WHERE userID={userID}')
        if len(cursor.fetchall()) == 0:
            flash('Invalid TechID entered')
            return redirect('/add_invoice')

        cursor.execute(f'SELECT VIN FROM CAR WHERE VIN="{vin}"')
        if len(cursor.fetchall()) == 0:
            flash('Invalid VIn entered, try again or add car')
            return redirect('/add_invoice')
  
        cursor.execute(f'''
            INSERT INTO INVOICE (userID, custID, VIN, repairNum, totalCost)
            VALUES ({userID}, {custID}, "{vin}", {repairNum}, {cost})
        ''')

        db.commit() 
        return redirect('/invoices')


@app.route('/invoice_paid', methods=['POST'])
def invoice_paid():

    invoiceNum = request.form['invoice']

    try:
        invoiceNum = int(invoiceNum)
    except ValueError:
        flash('Invalid invoice number to set paid')
        return redirect('/invoices')
   
    cursor.execute(f'''
        UPDATE INVOICE 
        SET paid=true
        WHERE invoiceNum={invoiceNum}
    ''')

    db.commit()
    
    return redirect('/invoices')


@app.route('/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'GET':
        webpage = render_template('employees.html')        
        cursor.execute(f''' SELECT * FROM EMPLOYEE ''')
        emps = cursor.fetchall()
        for emp in emps:
            webpage += f'''<p>
                UserID: {emp[0]}<br>
                Name: {emp[4]} {emp[5]}<br>
                Email: {emp[6]}<br>
                Hiredate: {emp[2]}<br>
                Store number: {emp[3]}<br>
                Payrate: {emp[1]}<br> 
            </p>'''
        return webpage

    elif request.method == 'POST':

        userid = request.form['userID']

        try:
            userid = int(userid)
        except ValueError:
            flash('Invalid UserID to remove')
            return redirect('/employees')

        cursor.execute(f''' DELETE FROM LOGIN WHERE userID={userid} ''')
        cursor.execute(f''' DELETE FROM EMPLOYEE WHERE userID={userid} ''')

        db.commit()
        return redirect('/employees')


@app.route('/about', methods=['GET', 'POST'])
def about():
    webpage = render_template('about.html')

    cursor.execute(f'''
        SELECT * FROM SHOP
    ''')

    result = cursor.fetchall()
    
    for shop in result:
        webpage += f'''
            Store {shop[0]}<br>
            Owner: {shop[1]}<br>
            Contact: {shop[2]}<br>
            {shop[5]}, {shop[3]}, {shop[4]}<br>
        '''

    return webpage


