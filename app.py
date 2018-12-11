#!/usr/bin/python2.7

from datetime import date
from flask import (Flask, render_template, request, url_for, redirect, flash)
import sys
import search_donation_history
import search_inventory_history
import donationBackend
import expenditureBackend

app = Flask(__name__)
app.secret_key = 'stringy string'

@app.route('/')
def index():
    conn = search_donation_history.getConn('c9')
    total = search_inventory_history.countInventoryTotal(conn)
    flash("Total Number of Inventory Items: " + str(total))
    return render_template('index.html')
    
@app.route("/donationForm/", methods=['GET', 'POST'])
def donationForm():
    '''
    Route for donation form page. 
    On GET, renders blank form.
    On POST, collects and validates data and if valid, adds to database. 
       Renders form again with submission confirmation flashed.
    '''
    if request.method == 'GET':
        return render_template('donation_form.html')
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
            for msg in val_result:
                flash(msg)
            return(redirect(url_for('donationForm')))
        
        #add donor to db, collect donorID
        donor_id = donationBackend.add_donor(donor)
        flash('Donor ID: ' + str(donor_id))
        
        #collect donation data
        donation = {
            'donor_id': donor_id,
            'submit_date': date.today(), 
            'description': request.form['donation-description'],
            'amount': request.form['amount'],
            'type': request.form['donation-category']
        }
        
        # validate donation data
        validation_result = donationBackend.validate_donation(donation)
        if len(validation_result) != 0:
            for msg in val_result:
                flash(msg)
            return(redirect(url_for('donationForm')))
        
        # send data to db
        donation_id = donationBackend.add_donation(donation)
        flash('Donation ID: '+ str(donation_id))
        
        #add donation to inventory
        inventory_id = donationBackend.add_to_inventory(donation)
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
        val_result = expenditureBackend.validate_expenditure(expenditure)
        if len(val_result) != 0:
            for msg in val_result:
                flash(msg)
            return(redirect(url_for('expenditureForm')))
           
        # Submit to Expenditure DB
        conn = donationBackend.get_conn('c9')
        expend_id = expenditureBackend.add_expend(expenditure, conn)
        flash('Expenditure ID: ' + str(expend_id))
        return render_template('expenditures.html')
 
    
#is not hooked up to the back end yet
@app.route('/updateInventory/', methods = ['GET', 'POST'])
def updateInventoryForm():
    conn = search_inventory_history.getConn('c9')
    allItemTypes = search_inventory_history.getInventoryItemTypes(conn)
    if request.method == 'GET':
        return render_template('updateInventory.html', inventory = allItemTypes)
        
    else:
        updatedItem = {
            'item_id' : request.form['item-type'],
            'amount' : request.form['item-amount'],
            'units' : request.form['item-units'],
            'date' : date.today()
        }
        return render_template('updateInventory.html', inventory = allItemTypes)


@app.route('/donations/', methods=["GET", "POST"])
def displayDonations():
    conn = search_donation_history.getConn('c9')
    allDonations = search_donation_history.getAllDonationHistoryInfo(conn, rowType='dictionary')
    return render_template('donations.html',allDonations= allDonations )
    

@app.route('/inventory/', methods=["GET", "POST"])
def displayInventory():
    conn = search_inventory_history.getConn('c9')
    allInventory = search_inventory_history.getAllInventoryHistoryInfo(conn) 
    return render_template('inventory.html', allInventory = allInventory)

    
@app.route('/filterDonationType/', methods=["GET", "POST"])
def filterDonationType():
    conn = search_donation_history.getConn('c9')
    selectedType = request.form.get("type")
    donationByType = search_donation_history.getDonationByType(conn, selectedType)
    if (len(donationByType) == 0):
        flash("There have been no donations of type: " + selectedType)
        return render_template('donations.html',allDonations = donationByType)
    else:
        return render_template('donations.html',allDonations = donationByType)


@app.route('/filterInventoryType/', methods=["GET", "POST"])
def filterInventoryType():
    conn = search_inventory_history.getConn('c9')
    selectedType = request.form.get("type")
    inventoryByType = search_inventory_history.getInventoryByType(conn, selectedType)
    if (len(inventoryByType) == 0):
        flash("There are no inventory items of type: " + selectedType)
    return render_template('inventory.html',allInventory = inventoryByType)


@app.route('/reset/', methods=['GET', 'POST'])
def reset():
    resetType = request.form.get("submit-btn")
    if (resetType == "Reset Inventory"):
        return redirect('inventory')
    else: 
        return redirect('donations')

    
@app.route('/sortBy/', methods=["GET", "POST"])
def sortBy():
    conn = search_donation_history.getConn('c9')
    selectedType = request.form.get("menu-tt")
    if (selectedType == "Most Recent Donation"):
        donationsOrdered = search_donation_history.sortDonationByDateDescending(conn)
        return render_template('donations.html',allDonations = donationsOrdered)
    elif (selectedType == "Oldest Donation First"):
        donationsOrdered = search_donation_history.sortDonationByDateAscending(conn)
        return render_template('donations.html',allDonations = donationsOrdered)
    elif (selectedType == "Donation Type"):
        donationsOrdered = search_donation_history.sortDonationType(conn)
        return render_template('donations.html',allDonations = donationsOrdered)
    # If selectedType is within inventory page:
    elif (selectedType == "Most Recent Item"):
        inventoryOrdered = search_inventory_history.sortInventoryByDateDescending(conn)
        return render_template('inventory.html',allInventory = inventoryOrdered)
    elif (selectedType == "Oldest Item First"):
        inventoryOrdered = search_inventory_history.sortInventoryByDateAscending(conn)
        return render_template('inventory.html',allInventory = inventoryOrdered)
    #If selectedType == "Item Type"....
    else: 
        inventoryOrdered = search_inventory_history.sortInventoryType(conn)
        return render_template('inventory.html',allInventory = inventoryOrdered)


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)