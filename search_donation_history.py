#!/usr/bin/python2.7

"""
Searches for the movie by title.
----------------------------------------------------------------
CS 304 - Databases 
Assignment 5
October, 2018
"""

import sys
import MySQLdb
from connection import get_conn

# def getConn(db):
#     """A function that opens a connection with the database
#     """
#     return MySQLdb.connect(host='localhost',
#                           user='cotequotey',
#                           passwd='',
#                           db=db)
    
    
def countDonationTotal(conn):
    """Returns total number donations"""
    curs = conn.cursor()
    curs.execute(
        '''select count(*) from donation''')
    return curs.fetchone()[0]
    
def countDonorTotal(conn):
    """Returns total number donors"""
    curs = conn.cursor()
    curs.execute(
        '''select count(*) from donor''')
    return curs.fetchone()[0]
    
                           
def getAllDonationHistoryInfo(conn):
    """Returns all donations, in the order they were 
    entered in the database."""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select description, donationID, submitDate, amount, units, type from donation''')
    return curs.fetchall()
    
def sortDonationByDateAscending(conn):
    """Returns all donations, in the order they were 
    entered in the database."""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select description, donationID, submitDate, amount, units, type 
        from donation order by submitDate asc''')
    return curs.fetchall()

def sortDonationByDateDescending(conn):
    """Returns all donations, in the order they were 
    entered in the database."""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select description, donationID, submitDate, amount, units, type 
        from donation order by submitDate desc''')
    return curs.fetchall()
    
def sortDonationType(conn):
    """Returns all donations, in the order they were 
    entered in the database."""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select description, donationID, submitDate, amount, units, type 
        from donation order by type''')
    return curs.fetchall()
    

def combineFilters(conn, filter, sort):
    """Returns the donations table after filtering and then sorting"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    if (sort == "Most Recent Donation"):
        curs.execute(
        '''select description, donationID, submitDate, amount, units, type from donation
        where `type` = %s order by submitDate desc''' ,[filter])
    elif (sort == "Most Recent Donation"):
        curs.execute(
        '''select description, donationID, submitDate, amount, units, type from donation
        where `type` = %s order by submitDate asc''' ,[filter])
    else: # If sorting by type alphabetically    
        curs.execute(
            '''select description, donationID, submitDate, amount, units, type from donation
            where `type` = %s order by type''' ,[filter])
    return curs.fetchall() 

def getDonationByType(conn, itemType):
    """Returns all donations of a specific type."""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select description, donationID, submitDate, 
    amount, units, type from donation where `type` = %s''', [itemType])
    return curs.fetchall()   

if __name__ == '__main__':
    conn = getConn('c9')
    allDonations = getDonationByType(conn, 'food')
    print allDonations