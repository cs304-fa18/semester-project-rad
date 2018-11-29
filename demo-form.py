from datetime import date
from flask import (Flask, url_for, redirect, request, render_template,
    flash, session, jsonify)
import donationDBOps
    
app = Flask("__name__")
app.secret_key = "replyall"

@app.route("/", methods=['GET', 'POST'])
def home():
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
        flash('Donor ID: ' + str(donor_id) + '\nDonation ID: '+ str(donation_id))
        
        #add donation to inventory
        donationDBOps.add_to_inventory(donation)
        
        return render_template('donation_form.html')
            
    
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 8081)