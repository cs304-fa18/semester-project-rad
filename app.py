#!/usr/bin/python2.7

from datetime import date
from flask import (Flask, render_template, request, url_for, redirect, flash)
import sys
import search_donation_history
# import search_inventory_history
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
            "name": request.form['donor-name'],
            'type': request.form['donor-type'],
            "phone": request.form['donor-phone'],
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

# Tried combining the functionality of displaying table with filtering by type 
# Might not be sustainable for other filtering criteria 
# Just tried this to see if it would work, and it didn't
# Gave this error: not all arguments converted during string formatting

# @app.route('/donations/', methods=["GET", "POST"])
# def displayDonations():
#     conn = search_donation_history.getConn('c9')
#     selectedType = request.form.get("menu-tt")
#     if selectedType == "Choose One":
#         allDonations = search_donation_history.getAllDonationHistoryInfo(conn, rowType='dictionary')
#     else:
#         allDonations = search_donation_history.getDonationByType(conn, selectedType)
#     return render_template('donations.html',allDonations= allDonations )
    
@app.route('/filterDonationType/', methods=["GET", "POST"])
def filterDonationType():
    conn = search_inventory_history.getConn('c9')
    selectedType = request.form.get("menu-tt")
    allDonations = search_donation_history.getDonationByType(conn, selectedType)
    #return redirect(url_for('displayDonations', allDonations = allDonations))
    return render_template('donations.html',allDonations = allDonations)
    # This one below I saw for Ajax?
    #return redirect(request.referrer) 
    
# Alternative is to use some Ajax like function I tried below, though unsure what to put in jsonify    
# @app.route('/filterDonationType/', methods=["POST"])
# def filterDonationType():
#     if request.method=="POST":
#         conn = search_inventory_history.getConn('c9')
#         selectedType = request.form.get("menu-tt")
#         allDonations = search_donation_history.getDonationByType(conn, selectedType)
#         return jsonify({'menu-tt':selectedType,??})

@app.route('/inventory/', methods=["GET", "POST"])
def displayInventory():
    conn = search_inventory_history.getConn('c9')
    allInventory = search_inventory_history.getAllInventoryHistoryInfo(conn, rowType='dictionary') 
    return render_template('inventory.html', allInventory = allInventory)

# Gives error: not all arguments converted during string formatting
@app.route('/filterInventoryType/', methods=["GET", "POST"])
def filterInventoryType():
    conn = search_donation_history.getConn('c9')
    selectedType = request.form.get("menu-tt")
    allInventory = search_inventory_history.getInventoryByType(conn, selectedType) 
    #return redirect(url_for('displayInventory', allInventory = allInventory))
    return render_template('inventory.html',allInventory = allInventory)
    # This one below I saw for Ajax?
    #return redirect(request.referrer)


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)
