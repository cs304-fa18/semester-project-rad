import MySQLdb
import re
import threading
from connection import get_conn
from threading import Lock
from search_inventory_history import updateInventory

# curs = conn.cursor(MySQLdb.cursors.DictCursor)


def add_donor(conn, donor_dict):
    '''
    Adds donor row to database
    Inputs:
        conn -- database connection
        donor_dict -- dictionary with keys: name, description, type, phone,
                     email, address
    Returns: id of newly added row in donor table
    '''

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
    curs.execute('''SELECT last_insert_id();''')
    result =curs.fetchone()
    return(result[0])


def add_donation(conn, donation_dict):
    '''
    Adds donation row to database
    Inputs:
       conn -- database connection
       donation_dict -- dictionary with keys: donor_id, submit_date, type, 
                        description, amount, units
    Returns: id of newly added row in donation table
    '''
    
    curs = conn.cursor()
    curs.execute('''INSERT INTO 
        donation(donorID, submitDate, description, amount, units, type)
        VALUES(%s, %s, %s, %s, %s, %s);''', [
                donation_dict['donor_id'],
                donation_dict['submit_date'],
                donation_dict['description'],
                donation_dict['amount'],
                donation_dict['units'],
                donation_dict['type']
            ])
    curs.execute('''SELECT last_insert_id();''')
    result =curs.fetchall()
    return(result[0][0])


def add_to_inventory(conn, donation_dict): 
    '''
    Checks if item already exists in inventory. In this case increments its
    amount in its database entry. If it doesn't exist, adds it to inventory
    Inputs:
        conn -- database connection
        donation_dict -- dictionary with keys: donor_id, submit_date, type, 
                        description, amount, units
    Returns: id of newly added/updated row in inventory table
    '''
    
    inventory_lock = Lock()
    inventory_lock.acquire()
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''SELECT count(*) FROM inventory 
        WHERE description like %s''', [ donation_dict['description']])
    match = curs.fetchall()
    # print(match)
    match = match[0]['count(*)']
    # print(match)
    
    # item not in inventory
    if (match==0):
        curs.execute('''INSERT INTO inventory(description, amount, units, status, type)
            VALUES (%s,%s,%s, %s, %s)''', [
                    donation_dict['description'],
                    donation_dict['amount'],
                    donation_dict['units'],
                    "NULL",
                    donation_dict['type']
                ])
        curs.execute('''SELECT last_insert_id();''')
        inventory_lock.release()
        result = curs.fetchall()
        # print(str(result))
        return(result[0]['last_insert_id()'])
    
    # item found in inventory previously
    else:
        curs.execute('''SELECT item_id, amount FROM inventory 
            WHERE description like %s 
            LIMIT 1;''',[ donation_dict['description']])
        match_row = curs.fetchall()
        # print(match_row)
        update_id = match_row[0]['item_id']
        new_amount = int(match_row[0]['amount']) + int(donation_dict['amount'])
        updateInventory(conn, update_id, new_amount)
        inventory_lock.release()
        # curs.execute('''UPDATE inventory 
        #     SET amount=%s WHERE item_id=%s''', [new_amount, update_id] )
        # # print(update_id)
        return(update_id)


def validate_donation(donation_dict):
    '''
    Validates donation data according to basic type expectations
    Inputs:
        donation_dict -- dictionary with donor_id, submit_date, description,
                         amount, type, units
    Returns: messages list with errors to flash. If list empty, data is valid
    '''
    
    messages = []
    categories = ['food','medical','clothing','supplies','money','other']
    if donation_dict['type'] not in categories:
        messages.append('Invalid donation category')
    
    try:
       x = int(donation_dict['amount'])
       if x <= 0:   
        messages.append("Invalid input: Amount donated must be positive nonzero number")
    except ValueError:
        messages.append("Invalid input: amount donated must be an integer")

    return messages
    

def validate_donor(donor_dict):
    '''
    Validates donor data according to basic type expectations
    Inputs:
        donor_dict -- dictionary with name, type, phone, email, address,
                      description
    Returns: messages list with errors to flash, if list empty, data is valid
    '''
    
    messages = []
    
    donor_types = ['individual', 'organization']
    if donor_dict['type'] not in donor_types:
        messages.append('Invalid donor type')
    # donor type in categories
    # phone is  10 digits
    if len(donor_dict['phone']) != 10:
        messages.append('Invalid phone number: must be 10 digits long')
    
    # email exists
    if donor_dict['email'] is None:
        messages.append('Invalid input: email address required')
    # email has exactly one @
    else:
        if (donor_dict['email'].count('@') != 1):
            messages.append('Invalid email address: must include exactly one @ symbol')
        else:
            # email matches pattern *@*.*
            pattern = '.*@.*[.].{2}.*'
            if (re.match(pattern, donor_dict['email']) is None):
                messages.append('Invalid email address format')
    return messages
 

def get_inventory_items(conn):  
    '''
    Inputs:
        conn -- database connection
    Returns: list of all items in inventory (id and name)
    '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''SELECT item_id as id, description FROM inventory;''')
    result = curs.fetchall()
    # print(result)
    return(result)


def get_donors(conn):
    '''
    Inputs:
        conn -- database connection
    Returns: list of all donors (id and name) from database
    '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''SELECT donorID as id, name FROM donor;''')
    result = curs.fetchall()
    # print(result)
    return(result)

    
def test_pattern():
    '''
    testing function for email regex pattern
    '''
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
    
    
if __name__ == '__main__':
    '''
    testing driver
    '''
    # add_to_inventory(
    #     {'description': 'pile of sticks', 'amount': 1, 'type': 'other'}
    # )
    # add_to_inventory(
    #     {'description': 'unknown donation', 'amount': 2, 'type': 'supplies'}
    # )
    
    #test_pattern()
    
    from connection import get_conn
    
    conn = get_conn()
    get_donors(conn)
    