from flask import (Flask, render_template, request,  url_for, redirect, flash)
import search_donation_history

app = Flask(__name__)

app.secret_key = 'You ll never guess this'

    
@app.route('/searchDonationHistory/')
def search():
    conn = search_donation_history.getConn('c9')
    allDonations = search_donation_history.getAllDonationHistoryInfo(conn) 
    
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)
    