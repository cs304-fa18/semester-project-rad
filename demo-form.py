from flask import (Flask, url_for, redirect, request, render_template,
    flash, session, jsonify)
    
app = Flask("__name__")
app.secret_key = "replyall"

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('donation_form.html')
    else:
        # collect data
        donor = {
            "name": request.form['donor-name'],
            'type': request.form['donor-type'],
            "phone": request.form['donor-phone'],
            'email': request.form['donor-email'],
            'address': request.form['donor-address'],
            'description': request.form['donor-description']
        }
        donation = {
            'item': request.form['item-type'],
            'amount': request.form['item-amount']
        }
        
        # validate data
        
        # send data to db
        return(str(request.form))
        
    
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 8081)