from flask import (Flask, url_for, redirect, request, render_template,
    flash, session, jsonify)
    
app = Flask("__name__")
app.secret_key = "replyall"

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('donation_form.html')
    else:
        return(str(request.form))
    
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 8081)