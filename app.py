#!/usr/bin/python2.7

from datetime import date
from flask import (Flask, render_template, request, url_for, redirect, flash)
import sys
import search_donation_history
import search_inventory_history
import donationDBOps

app = Flask(__name__)
app.secret_key = 'stringy string'

    
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route("/donationForm/", methods=['GET', 'POST'])
def donationForm():
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
        
        #add donor to db, collect donorID
        donor_id = donationDBOps.add_donor(donor)
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
        
        # send data to db
        donation_id = donationDBOps.add_donation(donation)
        flash('Donation ID: '+ str(donation_id))
        
        #add donation to inventory
        inventory_id = donationDBOps.add_to_inventory(donation)
        flash('Inventory ID: ' + str(inventory_id))
        
        # render template
        return render_template('donation_form.html')

@app.route('/donations/', methods=["GET", "POST"])
def displayDonations():
    conn = search_donation_history.getConn('c9')
    allDonations = search_donation_history.getAllDonationHistoryInfo(conn, rowType='dictionary')
    return render_template('donations.html',allDonations= allDonations )
    
@app.route('/reset/', methods=['GET', 'POST'])
def restDonationPage():
    return redirect('donations')
    
@app.route('/sortBy/', methods=["GET", "POST"])
def sortDonations():
    conn = search_donation_history.getConn('c9')
    selectedType = request.form.get("menu-tt")
    if (selectedType == "Most Recent Donation"):
        donationsOrdered = search_donation_history.sortDonationByDateDescending(conn)
        return render_template('donations.html',allDonations = donationsOrdered)
    elif (selectedType == "Oldest Donation First"):
        donationsOrdered = search_donation_history.sortDonationByDateAscending(conn)
        return render_template('donations.html',allDonations = donationsOrdered)
    else:
        donationsOrdered = search_donation_history.sortDonationType(conn)
        return render_template('donations.html',allDonations = donationsOrdered)
    
@app.route('/filterDonationType/', methods=["GET", "POST"])
def filterDonationType():
    conn = search_donation_history.getConn('c9')
    selectedType = request.form.get("menu-tt")
    donationByType = search_donation_history.getDonationByType(conn, selectedType)
    if (len(donationByType) == 0):
        flash("There have been no donations of type: " + selectedType)
        return render_template('donations.html',allDonations = donationByType)
    else:
        return render_template('donations.html',allDonations = donationByType)

@app.route('/inventory/', methods=["GET", "POST"])
def displayInventory():
    conn = search_inventory_history.getConn('c9')
    allInventory = search_inventory_history.getAllInventoryHistoryInfo(conn) 
    return render_template('inventory.html', allInventory = allInventory)

# Gives error: not all arguments converted during string formatting
@app.route('/filterInventoryType/', methods=["GET", "POST"])
def filterInventoryType():
    conn = search_inventory_history.getConn('c9')
    selectedType = request.form.get("type")
    inventoryByType = search_inventory_history.getInventoryByType(conn, selectedType)
    return render_template('inventory.html',allInventory = inventoryByType)


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)