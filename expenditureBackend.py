import MySQLdb
from connection import get_conn

def countExpenditureTotal(conn):
    """Returns the number of items in inventory"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select count(*) from expenditure''')
    return curs.fetchall()[0]['count(*)']

def add_expend(conn, expenditure):
    '''
    Adds expenditure row to database
    Inputs:
       expenditure -- dictionary containing keys date, expenditure-description,
                      amount, expenditure-category
        conn -- database connection
    Return value: id of newly added row in expenditure table
    '''
    
    curs = conn.cursor()
    curs.execute('''INSERT INTO 
        expenditure(date, description, amount, type)
        VALUES(%s, %s, %s, %s);''', [
                expenditure['date'],
                expenditure['expenditure-description'],
                expenditure['amount'],
                expenditure['expenditure-category']
            ])
    curs.execute('''SELECT last_insert_id() FROM expenditure;''')
    result =curs.fetchall()
    # print(result)
    return(result[0][0])

    
def validate_expenditure(expend_dict):
    '''
        Validates expenditure data according to expectations
        Inputs: 
           expend_dict - dictionary with keys: expenditure-category, amount,
                         expenditure-description, date
        Returns: messages list with errors. If list empty, data is valid.
    '''
    messages = []
    # check expenditure-category in list of valid values
    categories = ['food','medical','clothing','supplies','in house','other']
    if expend_dict['expenditure-category'] not in categories:
        messages.append("Invalid input: expenditure category")
    # amount is an int, positive
    if not isinstance(expend_dict['amount'], int):
        messages.append("Invalid input: Amount spent must be integer.")
    elif expend_dict['amount'] <= 0:
        messages.append("Invalid input: Amount spent must be positive nonzero number.")
    return(messages)
    

def test_validate_expenditure():
    '''
    testing cases
    '''
    good_set = {
        'expenditure-category' : 'food',
        'amount' : 42,
        'expenditure-description' : 'some food'
    }
    print(validate_expenditure(good_set))
    
    bad_set1 = {
        'expenditure-category' : 'rofl',
        'amount' : 42,
        'expenditure-description' : 'some food'
    }
    print(validate_expenditure(bad_set1))
    
    bad_set2 = {
    'expenditure-category' : 'food',
    'amount' : '42forty two',
    'expenditure-description' : 'some food'
    }
    print(validate_expenditure(bad_set2))
    
    bad_set3 = {
        'expenditure-category' : 'food',
        'amount' : -3,
        'expenditure-description' : 'some food'
    }
    print(validate_expenditure(bad_set3))
    

if __name__ == '__main__':
    '''
    testing driver
    '''
    test_validate_expenditure()
    