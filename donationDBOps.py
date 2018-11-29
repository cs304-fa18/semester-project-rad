import MySQLdb

def get_conn(db):
    c = MySQLdb.connect(host='localhost',
                           user='arivera4',
                           passwd='',
                           db=db)
    c.autocommit(True)
    return c

#    curs = conn.cursor(MySQLdb.cursors.DictCursor)


def add_donor(donor_dict):
    conn = get_conn('c9')
    curs = conn.cursor()
    curs.execute('''INSERT INTO donor(name, description, type, phoneNum, email, address)
        VALUES(%s, %s, %s, %s, %s, %s);''', [
            donor_dict['name'], 
            donor_dict['description'],
            donor_dict['type'],
            donor_dict['phone'],
            donor_dict['email'],
            donor_dict['address']
        ])
    curs.execute('''SELECT max(donorID) FROM donor;''')
    result =curs.fetchall()
    return(result[0][0])

def add_donation(donation_dict):
    conn = get_conn('c9')
    curs = conn.cursor()
    curs.execute('''INSERT INTO donation(donorID, submitDate, description, amount, type)
        VALUES(%s, %s, %s, %s, %s);''', [
                donation_dict['donor_id'],
                donation_dict['submit_date'],
                donation_dict['description'],
                donation_dict['amount'],
                donation_dict['type'],
            ])
    curs.execute('''SELECT max(donationID) FROM donation;''')
    result =curs.fetchall()
    return(result[0][0])