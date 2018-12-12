#!/usr/bin/python2.7

from datetime import date
from flask import (Flask, render_template, request, url_for, redirect, flash)
import sys
import search_donation_history
import search_inventory_history
import donationBackend
import expenditureBackend
from connection import get_conn

app = Flask(__name__)
app.secret_key = 'stringy string'

@app.route('/')
def index():
    conn = get_conn()
    total = search_inventory_history.countInventoryTotal(conn)
    mediumCount = search_inventory_history.statusCount(conn, "medium")
    lowCount = search_inventory_history.statusCount(conn, "low")
    highCount = search_inventory_history.statusCount(conn, "high")
    flash("INVENTORY AT A GLANCE: ")
    flash("Total Items: " + str(total))
    flash("STATUS COUNT: ")
    flash( "Total Low:" + str(lowCount))
    flash( "Total Medium:" + str(mediumCount))
    flash( "Total High:" + str(highCount))
    return render_template('index.html')
    
@app.route("/donationForm/", methods=['GET', 'POST'])
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
        donation_list = donationBackend.get_donations(conn)
        return render_template('donation_form.html', donor_list=donor_list, donation_list=donation_list)
    else:
        existing_id = request.form['existing-donor']
        if existing_id is not '':
            donor_id = existing_id
            print(existing_id)
            
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
            flash('Donor ID: ' + str(donor_id))
        
        
        #collect donation data
        description = request.form['existing-donation']
        if request.form['existing-donation'] is '':
            description = request.form['donation-description']
            
        donation = {
            'donor_id': donor_id,
            'submit_date': date.today(), 
            'description': description,
            'amount': request.form['amount'],
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
        flash('Donation ID: '+ str(donation_id))
        
        #add donation to inventory
        inventory_id = donationBackend.add_to_inventory(conn, donation)
        flash('Inventory ID: ' + str(inventory_id))
        
        # render template
        return render_template('donation_form.html')



@app.route('/expenditureForm/', methods = ['GET', 'POST'])
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
            'amount' : request.form['item-amount'],
            'date' : date.today()
        }
    return render_template('updateInventory.html', inventory = allItemTypes)


@app.route('/donations/', methods=["GET", "POST"])
def displayDonations():
    conn = get_conn()
    allDonations = search_donation_history.getAllDonationHistoryInfo(conn, rowType='dictionary')
    return render_template('donations.html',allDonations= allDonations )
    

@app.route('/inventory/', methods=["GET", "POST"])
def displayInventory():
    conn = get_conn()
    allInventory = search_inventory_history.getAllInventoryHistoryInfo(conn) 
    return render_template('inventory.html', allInventory = allInventory)
    
@app.route('/reset/', methods=['GET', 'POST'])
def reset():
    resetType = request.form.get("submit-reset")
    if (resetType == "Reset Inventory"):
        return redirect('inventory')
    else: 
        return redirect('donations')
        
@app.route('/filterDonations/sortBy/', methods=["GET", "POST"])
def filterDonations():
    conn = get_conn()
    dropdownType = request.form.get("menu-tt")
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
            if (dropdownType == "Most Recent Item"):
                donationsOrdered = search_donation_history.sortDonationByDateDescending(conn)
                return render_template('donations.html',allDonations = donationsOrdered)
            elif (dropdownType == "Oldest Item First"):
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
    conn = get_conn()
    dropdownType = request.form.get("menu-tt")
    checkboxType = request.form.get("type")
    inventoryByStatus = search_inventory_history.getInventoryByStatus(conn, dropdownType)
    inventoryByType = search_inventory_history.getInventoryByType(conn, checkboxType)
    allInventory = search_inventory_history.getAllInventoryHistoryInfo(conn)
    
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
            if (dropdownType == "Ascending Status"):
                sortInventory = search_inventory_history.getInventoryByStatus(conn, dropdownType)
                return render_template('inventory.html',allInventory = sortInventory)
            else:
                sortInventory = search_inventory_history.sortInventoryType(conn)
                return render_template('inventory.html',allInventory = sortInventory)
        #Drop down and checkbox both selected! 
        else:
            filtered = search_inventory_history.combineFilters(conn, checkboxType,dropdownType)
            return render_template('inventory.html',allInventory = filtered)


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)