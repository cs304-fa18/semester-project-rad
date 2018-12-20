#!/usr/bin/python2.7

from datetime import date
from flask import (Flask, render_template, request, url_for, redirect, flash, session)
import bcrypt
import sys
import MySQLdb
import search_donation_history
import search_inventory_history
import donationBackend
import expenditureBackend
from connection import get_conn
from functools import wraps

app = Flask(__name__)
app.secret_key = 'stringy string'

#login decorator         
def login_required(f):
    @wraps(f)
    def wrap():
        if 'logged_in' in session:
            return f()
        else:
            flash("You need to login first")
            return redirect(url_for('index'))
    return wrap
           
@app.route('/')
def index():
    conn = get_conn()
    inventoryTotal = search_inventory_history.countInventoryTotal(conn)
    lowList = search_inventory_history.listLowItems(conn)
    lastWeekDonations = search_donation_history.donationsPastWeek(conn)
    lowCount = search_inventory_history.statusCount(conn, "low")
    highCount = search_inventory_history.statusCount(conn, "high")
    donationTotal = search_donation_history.countDonationTotal(conn)
    donorTotal = search_donation_history.countDonorTotal(conn)
    expenditureTotal = expenditureBackend.countExpenditureTotal(conn)
    mostSpent = expenditureBackend.mostExpensiveType(conn)
    leastSpent = expenditureBackend.leastExpensiveType(conn)
    return render_template(
        'index.html', 
        inventoryTotal=inventoryTotal, 
        lowList = lowList, 
        lowCount = lowCount, 
        highCount=highCount, 
        lastWeekDonations=lastWeekDonations,
        donationTotal=donationTotal, 
        donorTotal=donorTotal, 
        expenditureTotal=expenditureTotal, 
        mostSpent = mostSpent, 
        leastSpent = leastSpent
    ) 
   
@app.route("/donationForm/", methods=['GET', 'POST'])
@login_required
def donationForm():
    '''
    Route for donation form page. 
    On GET, renders blank form.
    On POST, collects and validates data and if valid, adds to database. 
       Renders form again with submission confirmation flashed.
    '''

    conn = get_conn()
    
    if request.method == 'GET':
        donor_list = donationBackend.get_donors(conn)
        donation_list = donationBackend.get_inventory_items(conn)
        return render_template('donation_form.html', donor_list=donor_list, donation_list=donation_list)
    else:
        existing_id = request.form['existing-donor']
        if existing_id != "create-new-donor":
            donor_id = existing_id
            # print('***********Existing ID: ' + existing_id)
            
        else:
            # collect donor data
            donor = {
                'name': request.form['donor-name'],
                'type': request.form['donor-type'],
                'phone': request.form['donor-phone'],
                'email': request.form['donor-email'],
                'address': request.form['donor-address'],
                'description': request.form['donor-description']
            }
            
            #validate donor data
            validation_result = donationBackend.validate_donor(donor)
            if len(validation_result) != 0:
                for msg in validation_result:
                    flash(msg)
                return(redirect(url_for('donationForm')))
            
            #add donor to db, collect donorID
            donor_id = donationBackend.add_donor(conn, donor)
            # print("*************DONOR ID: " + str(donor_id))
            flash('New donor created. ID: ' + str(donor_id))
        
        
        #collect donation data
        
        description = request.form['existing-donation']
        if request.form['existing-donation'] == 'create-new-donation':
            description = request.form['donation-description']
            amount = request.form['amount']
        else:
            amount = request.form['left-amount']
        
            
        donation = {
            'donor_id': donor_id,
            'submit_date': date.today(), 
            'description': description,
            'amount': amount,
            'units': request.form['units'],
            'type': request.form['donation-category']
        }
        
        # validate donation data
        validation_result = donationBackend.validate_donation(donation)
        if len(validation_result) != 0:
            for msg in validation_result:
                flash(msg)
            return(redirect(url_for('donationForm')))
        
        # send data to db
        donation_id = donationBackend.add_donation(conn, donation)
        flash('Thank you for your donation! ID: '+ str(donation_id))
        
        #add donation to inventory
        inventory_id = donationBackend.add_to_inventory(conn, donation)
        flash('Inventory ID: ' + str(inventory_id))
        
        # render template
        donor_list = donationBackend.get_donors(conn)
        donation_list = donationBackend.get_inventory_items(conn)
        return render_template(
            'donation_form.html',
            donor_list=donor_list, 
            donation_list=donation_list
        )

@app.route('/sandbox/', methods=['GET', 'POST'])
def sandbox():
    conn = get_conn()
    donor_list = donationBackend.get_donors(conn)
    donation_list = donationBackend.get_inventory_items(conn)
    return render_template(
        'donation_form.html', donor_list=donor_list, donation_list=donation_list
    )

@app.route('/expenditureForm/', methods = ['GET', 'POST'])
@login_required
def expenditureForm():
    '''
    Route for exenditure form page. 
    On GET, renders blank form.
    On POST, collects and validates data and if valid, adds to database. 
       Renders form again with submission confirmation flashed.
    '''
            
    if request.method == 'GET':
        return render_template('expenditures.html')
        
    else:
    # Collect Expenditure Data
        expenditure = {
            'expenditure-category' : request.form['expenditure-category'],
            'amount' : request.form['expenditure-amount'],
            'expenditure-description' : request.form['expenditure-description'],
            'date' : date.today()
        }
        
        # Validate Expenditure Data
        validation_result = expenditureBackend.validate_expenditure(expenditure)
        if len(validation_result) != 0:
            for msg in validation_result:
                flash(msg)
            return(redirect(url_for('expenditureForm')))
           
        # Submit to Expenditure DB
        conn = get_conn()
        expend_id = expenditureBackend.add_expend(expenditure, conn)
        flash('Expenditure ID: ' + str(expend_id))
        return render_template('expenditures.html')
 
    
@app.route('/updateInventory/', methods = ['GET', 'POST'])
@login_required
def updateInventoryForm():
    '''Collects information from update inventory form
    passes this information to backend to update inventory table'''
    
    conn = get_conn()
    allItemTypes = search_inventory_history.getInventoryItemTypes(conn)
    
    if request.method == 'GET':
        return render_template('updateInventory.html', inventory = allItemTypes)
        
    else:
        updatedItem = {
            'item_id' : request.form['inventoryItem'],
            'amount' : request.form['new-amount'],
            'threshold' : request.form['new-threshold'],
            'date' : date.today()
        }
    
    #ensures an amount is entered for threshold if current value is none
    if updatedItem['threshold'] == "":
        currentStatus = search_inventory_history.getStatus(conn, updatedItem['item_id'])
    
        if (currentStatus[0]['status'] == "null"):
            flash("Please set a threshold for item " + updatedItem['item_id'])
            return(redirect(url_for('updateInventoryForm')))
    
    flash('Inventory item ' + updatedItem['item_id'] + ' Updated')    
    search_inventory_history.updateInventory(conn, updatedItem['item_id'], updatedItem['amount'], updatedItem['threshold'])
    return render_template('updateInventory.html', inventory = allItemTypes)


@app.route('/donations/', methods=["GET", "POST"])
@login_required
def displayDonations():
    '''displays all donations in a table on donations page'''
    conn = get_conn()
    allDonations = search_donation_history.getAllDonationHistoryInfo(conn)
    return render_template('donations.html',allDonations= allDonations )


@app.route('/inventory/', methods=["GET", "POST"])
@login_required
def displayInventory():
    '''displays all inventory in a table on inventory page'''
        
    conn = get_conn()
    allInventory = search_inventory_history.getInventoryItemTypes(conn) 
    return render_template('inventory.html', allInventory = allInventory)

    
@app.route('/reset/', methods=['GET', 'POST'])
def reset():
    '''clears all filters and sorting and displays original tables'''
    resetType = request.form.get("submit-reset")
    if (resetType == "Reset Inventory"):
        return redirect('inventory')
    else: 
        return redirect('donations')
 
        
@app.route('/filterDonations/sortBy/', methods=["GET", "POST"])
def filterDonations():
    '''Route that deals with all sorting and filtering of donations table'''
    conn = get_conn()
    dropdownType = request.form.get("menu-tt")
    print dropdownType
    checkboxType = request.form.get("type")
    donationByType = search_donation_history.getDonationByType(conn, checkboxType)
    allDonations = search_donation_history.getAllDonationHistoryInfo(conn)
    

    if dropdownType == "none": #No drop down selected
        #No drop down or checkboxes are selected
        if checkboxType is None: 
            return render_template('donations.html', allDonations = allDonations)
            
        else: #No drop down selected but at least one checkbox selected
            if (len(donationByType) == 0): #No items of checkboxType
                flash("There are no donations of type: " + checkboxType)
            return render_template('donations.html',allDonations = donationByType)
            
    else:# Drop down is selected
        #Drop down selected but not checkbox
        if checkboxType is None:
            if (dropdownType == "Most Recent Donation"):
                donationsOrdered = search_donation_history.sortDonationByDateDescending(conn)
                return render_template('donations.html',allDonations = donationsOrdered)
            elif (dropdownType == "Oldest Donation First"):
                donationsOrdered = search_donation_history.sortDonationByDateAscending(conn)
                return render_template('donations.html',allDonations = donationsOrdered)
            else:
                donationsOrdered = search_donation_history.sortDonationType(conn)
                return render_template('donations.html',allDonations = donationsOrdered)
        #Drop down and checkbox both selected! 
        else:
            filtered = search_donation_history.combineFilters(conn, checkboxType,dropdownType)
            return render_template('donations.html',allDonations = filtered)

@app.route('/filterInventory/sortBy/', methods=["GET", "POST"])
def filterInventory():
    '''Route that deals with all sorting and filtering of inventory table'''
    conn = get_conn()
    dropdownType = request.form.get("menu-tt")
    print dropdownType
    checkboxType = request.form.get("type")
    inventoryByType = search_inventory_history.getInventoryByType(conn, checkboxType)
    allInventory = search_inventory_history.getInventoryItemTypes(conn)
    
    if dropdownType == "none": #No drop down selected
        #No drop down or checkboxes are selected
        if checkboxType is None: 
            return render_template('inventory.html', allInventory = allInventory)
            
        else: #No drop down selected but at least one checkbox selected
            if (len(inventoryByType) == 0): #No items of checkboxType
                flash("There are no inventory items of type: " + checkboxType)
            return render_template('inventory.html',allInventory = inventoryByType)
            
    else:# Drop down is selected
        #Drop down selected but not checkbox
        if checkboxType is None:
            if dropdownType == "Status (Low to High)":
                sortInventory = search_inventory_history.sortInventoryStatus(conn)
                return render_template('inventory.html',allInventory = sortInventory)
            else:
                sortInventory = search_inventory_history.sortInventoryType(conn)
                return render_template('inventory.html',allInventory = sortInventory)
        #Drop down and checkbox both selected! 
        else:
            filtered = search_inventory_history.combineFilters(conn, checkboxType,dropdownType)
            return render_template('inventory.html',allInventory = filtered)

#renders login/join page
@app.route('/loginPage/',methods=["POST"])  
def redirectLogin():
    '''renders login.html where user can login or join'''
    return render_template('login.html')
    
@app.route('/join/', methods=["POST"])
def join():
    '''allows user to join by creating a username and password, checks if username is
    unique, encyrpts passwords and stores it'''
    try:
        username = request.form['username']
        passwd1 = request.form['password1']
        passwd2 = request.form['password2']
        if passwd1 != passwd2:
            flash('passwords do not match')
            return redirect( url_for('index'))
        hashed = bcrypt.hashpw(passwd1.encode('utf-8'), bcrypt.gensalt())
        conn = get_conn()
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT username FROM userpass WHERE username = %s',
                     [username])
        row = curs.fetchone()
        if row is not None:
            flash('That username is taken')
            return redirect( url_for('index') )
        curs.execute('INSERT into userpass(username,hashed) VALUES(%s,%s)',
                     [username, hashed])
        session['username'] = username
        session['logged_in'] = True
        flash('successfully logged in as '+username)
        return redirect( url_for('index') )
    except Exception as err:
        flash('form submission error '+str(err))
        return redirect( url_for('index') )
    
        
@app.route('/login/', methods=["POST"])
def login():
    '''allows user to login, confirms username and password combination are valid'''
    try:
        username = request.form['username']
        passwd = request.form['password']
        conn = get_conn()
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT hashed FROM userpass WHERE username = %s',
                     [username])
        row = curs.fetchone()
        if row is None:
            # Same response as wrong password, so no information about what went wrong
            flash('login incorrect. Try again or join')
            return redirect( url_for('index'))
        hashed = row['hashed']
        # strings always come out of the database as unicode objects
        if bcrypt.hashpw(passwd.encode('utf-8'),hashed.encode('utf-8')) == hashed:
            flash('successfully logged in as '+username)
            session['username'] = username
            session['logged_in'] = True
            return redirect( url_for('index'))
        else:
            flash('login incorrect. Try again or join')
            return redirect( url_for('index'))
    except Exception as err:
        flash('form submission error '+str(err))
        return redirect( url_for('index') )
        
@app.route('/logout/', methods=["POST"])
def logout():
    '''logouts current user'''
    try:
        if 'username' in session:
            username = session['username']
            session.pop('username')
            session.pop('logged_in')
            flash('You are logged out')
            return redirect(url_for('index'))
        else:
            flash('you are not logged in. Please login or join')
            return redirect( url_for('index') )
    except Exception as err:
        flash('some kind of error '+str(err))
        return redirect( url_for('index') )
        
  
        


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)