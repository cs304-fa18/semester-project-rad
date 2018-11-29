import MySQL
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