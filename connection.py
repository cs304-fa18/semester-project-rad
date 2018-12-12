import MySQLdb

def get_conn(db='c9'):
    c = MySQLdb.connect(host='localhost',
                           user='arivera4',
                           passwd='',
                           db=db)
    c.autocommit(True)
    return c