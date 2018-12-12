import MySQLdb

def get_conn(db='c9'):
    c = MySQLdb.connect(host='localhost',
                           user='hweissma',
                           passwd='',
                           db=db)
    c.autocommit(True)
    return c