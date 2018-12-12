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

def getConn(db):
    """A function that opens a connection with the database
    """
    return MySQLdb.connect(host='localhost',
                           user='cotequotey',
                           passwd='',
                           db=db)
                    
                           
def getAllDonationHistoryInfo(conn, rowType='dictionary'):
    """Returns all donations, in the order they were 
    entered in the database."""
    if rowType == "tuple":
        curs = conn.cursor()
    elif rowType == "dictionary":
        # results as Dictionaries
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select description, donationID, submitDate, amount, units, type from donation''')
    return curs.fetchall()
    
def sortDonationByDateAscending(conn, rowType='dictionary'):
    """Returns all donations, in the order they were 
    entered in the database."""
    if rowType == "tuple":
        curs = conn.cursor()
    elif rowType == "dictionary":
        # results as Dictionaries
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select description, donationID, submitDate, amount, units, type 
        from donation order by submitDate asc''')
    return curs.fetchall()

def sortDonationByDateDescending(conn, rowType='dictionary'):
    """Returns all donations, in the order they were 
    entered in the database."""
    if rowType == "tuple":
        curs = conn.cursor()
    elif rowType == "dictionary":
        # results as Dictionaries
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select description, donationID, submitDate, amount, units, type 
        from donation order by submitDate desc''')
    return curs.fetchall()
    
def sortDonationType(conn, rowType='dictionary'):
    """Returns all donations, in the order they were 
    entered in the database."""
    if rowType == "tuple":
        curs = conn.cursor()
    elif rowType == "dictionary":
        # results as Dictionaries
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select description, donationID, submitDate, amount, units, type 
        from donation order by type''')
    return curs.fetchall()
    
#Not sure if this will be used in the frontend, but maybe in the backend 
def getDonationByDonorID(conn, donorID, rowType='dictionary'):
    """Returns all donations given by a specific donorID."""
    if rowType == "tuple":
        curs = conn.cursor()
    elif rowType == "dictionary":
        # results as Dictionaries
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select donationID, submitDate, 
    amount, type from donation where donorID = %s''', [donorID])
    return curs.fetchall()

def combineFilters(conn, filter, sort):
    """Returns the donations table after filtering and then sorting"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select description, donationID, submitDate, amount, units, type from donation
        where `type` = %s order by %s''' ,[filter,sort])
    return curs.fetchall() 

def getDonationByDonorName(conn, donorName, rowType='dictionary'):
    """Returns all donations given by a specific donor."""
    if rowType == "tuple":
        curs = conn.cursor()
    elif rowType == "dictionary":
        # results as Dictionaries
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select donationID, submitDate, 
    amount, units, type from donation where donationID = %s''', ["%"+donorName+"%"])
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