from flask import (Flask, render_template, request,  url_for, redirect, flash)
import search_donation_history

app = Flask(__name__)

app.secret_key = 'You ll never guess this'

    
# @app.route('/allDonations/')
# def all():
#     conn = search_donation_history.getConn('c9')
#     allDonations = search_donation_history.getAllDonationHistoryInfo(conn) 
#     return redirect(url_for('displayDonations', displayed = allDonations))


# @app.route('/filter_by_type/')    
# def filterByType():
#     selectedType = request.form.get('menu-tt')
#     return redirect(url_for('displayDonations', displayed = selectedType))

@app.route('/')
def displayDonations():
    conn = search_donation_history.getConn('c9')
    allDonations = search_donation_history.getAllDonationHistoryInfo(conn) 
    return render_template('searchDonationHistory.html', history = allDonations)


    
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)
    