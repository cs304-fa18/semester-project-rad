import MySQLdb
import re

def get_conn(db):
    c = MySQLdb.connect(host='localhost',
                           user='arivera4',
                           passwd='',
                           db=db)
    c.autocommit(True)
    return c

# curs = conn.cursor(MySQLdb.cursors.DictCursor)


def add_donor(donor_dict):
    conn = get_conn('c9')
    curs = conn.cursor()
    curs.execute(
        '''INSERT INTO donor(name, description, type, phoneNum, email, address)
        VALUES(%s, %s, %s, %s, %s, %s);''', [
            donor_dict['name'], 
            donor_dict['description'],
            donor_dict['type'],
            donor_dict['phone'],
            donor_dict['email'],
            donor_dict['address']
        ]
    )
    curs.execute('''SELECT max(donorID) FROM donor;''')
    result =curs.fetchall()
    return(result[0][0])

def add_donation(donation_dict):
    conn = get_conn('c9')
    curs = conn.cursor()
    curs.execute('''INSERT INTO 
        donation(donorID, submitDate, description, amount, type)
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

def add_to_inventory(donation_dict): #surely there is a better way to do this? standardize caps?
    conn = get_conn('c9')
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''SELECT count(*) FROM inventory 
        WHERE description like %s''', [ donation_dict['description']])
    match = curs.fetchall()
    # print(match)
    match = match[0]['count(*)']
    # print(match)
    
    # item not in inventory
    if (match==0):
        curs.execute('''INSERT INTO inventory(description, status, type)
            VALUES (%s,%s,%s)''', [
                    donation_dict['description'],
                    donation_dict['amount'],
                    donation_dict['type']
                ])
        curs.execute('''SELECT max(item_id) FROM inventory;''')
        result = curs.fetchall()
        print(str(result))
        return(result[0]['max(item_id)'])
    
    # item found in inventory previously
    else:
        curs.execute('''SELECT item_id, status FROM inventory 
            WHERE description like %s 
            LIMIT 1;''',[ donation_dict['description']])
        match_row = curs.fetchall()
        # print(match_row)
        update_id = match_row[0]['item_id']
        new_status = int(match_row[0]['status']) + int(donation_dict['amount'])
        curs.execute('''UPDATE inventory 
            SET status=%s WHERE item_id=%s''', [new_status, update_id] )
        # print(update_id)
        return(update_id)

def validate_donation(donation_dict):
    '''
    input dict with keys: donor_id, submit_date, description, amount, type
    output: messages list with errors to flash. If list empty, green light
    '''
    
    messages = []
    categories = ['food','medical','clothing','supplies','money','other']
    if donation_dict['type'] not in categories:
        messages.append('Invalid donation category')
    
    if not isinstance(donation_dict['amount'], int):
        messages.append("Invalid input: Amount spent must be integer.")
    elif donation_dict['amount'] <= 0:
        messages.append("Invalid input: Amount spent must be positive nonzero number.")
    
    return messages
    

def validate_donor(donor_dict):
    #  donor = {
    #         'name': request.form['donor-name'],
    #         'type': request.form['donor-type'],
    #         'phone': request.form['donor-phone'],
    #         'email': request.form['donor-email'],
    #         'address': request.form['donor-address'],
    #         'description': request.form['donor-description']
    #     }
    messages = []
    
    donor_types = ['individual', 'organization']
    if donor_dict['type'] not in donor_types:
        messages.append('Invalid donor type')
    # donor type in categories
    # phone is  10 digits
    if len(donor_dict['phone']) != 10:
        messages.append('Invalid phone number: must be 10 digits long')
    # email has exactly one @
    if (donor_dict['email'].count('@') != 1):
        messages.append('Invalid email address: must include exactly one @ symbol')
    else:
        # email matches pattern *@*.*
        pattern = '.*@.*[.].{2}.*'
        if (re.match(pattern, donor_dict['email']) is None):
            messages.append('Invalid email address format')
    return messages
    
def test_pattern():
    pattern = '.*@.*[.].{2}.*'
    print('expected pass')
    print(re.match(pattern, "arivera4@wellesley.edu"))
    print('expected fail')
    print(re.match(pattern, "bademail.c"))
    print('expected fail')
    print(re.match(pattern, "bemamil.com"))
    print('expected fail')
    print(re.match(pattern, "justaword"))
    print('expected fail')
    print(re.match(pattern, "just a word . word"))
    
    

#testing driver
if __name__ == '__main__':
    # add_to_inventory(
    #     {'description': 'pile of sticks', 'amount': 1, 'type': 'other'}
    # )
    # add_to_inventory(
    #     {'description': 'unknown donation', 'amount': 2, 'type': 'supplies'}
    # )
    
    test_pattern()