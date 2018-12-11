import donationDBOps
import MySQLdb

def add_expend(expenditure, conn):
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
    print(result)
    return(result[0][0])
