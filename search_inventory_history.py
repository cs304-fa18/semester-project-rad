#!/usr/bin/python2.7

"""
Searches for the movie by title.
----------------------------------------------------------------
CS 304 - Databases 
RAD P3
"""

import sys
import MySQLdb

def getConn(db):
    """A function that opens a connection with the database
    """
    return MySQLdb.connect(host='localhost',
                           user='arivera4',
                           passwd='',
                           db=db)
                    
def countInventoryTotal(conn):
    """Returns all inventory, in order of last modified.
    since there could be none of an item, but then more added, 
    so updates should be first"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select count(*) from inventory''')
    return curs.fetchall()[0]['count(*)']
    
def getAllInventoryHistoryInfo(conn):
    """Returns all inventory, in order of last modified.
    since there could be none of an item, but then more added, 
    so updates should be first"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select item_id, submitDate, description, status, amount, units, `type` from inventory''')
    return curs.fetchall()
    
def sortInventoryByDateAscending(conn, rowType='dictionary'):
    """Returns all inventory, in the order they were 
    entered in the database."""
    if rowType == "tuple":
        curs = conn.cursor()
    elif rowType == "dictionary":
        # results as Dictionaries
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(
        '''select item_id, submitDate, description, status, amount, units, `type` from inventory
        order by submitDate asc''')
    return curs.fetchall()

def sortInventoryByDateDescending(conn, rowType='dictionary'):
    """Returns all donations, in the order they were 
    entered in the database."""
    if rowType == "tuple":
        curs = conn.cursor()
    elif rowType == "dictionary":
        # results as Dictionaries
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(
        '''select item_id, submitDate, description, status, amount, units, `type` from inventory
        order by submitDate desc''')
    return curs.fetchall()
    
def sortInventoryType(conn, rowType='dictionary'):
    """Returns all donations, in the order they were 
    entered in the database."""
    if rowType == "tuple":
        curs = conn.cursor()
    elif rowType == "dictionary":
        # results as Dictionaries
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select item_id, submitDate, description, status, amount, units, `type` from inventory
        order by type''')
    return curs.fetchall()
    
def getAllInventoryDescription(conn):
    """Returns all inventory, in order of last modified.
    since there could be none of an item, but then more added, 
    so updates should be first"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select item_id, submitDate, description, status, amount, units,`type` from inventory''')
    return curs.fetchall()

def getInventoryItemTypes(conn):
    '''Returns all inventory types, used in update inventory form'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select description, item_id from inventory''')
    return curs.fetchall()
    
                               
def getInventoryByStatus(conn, status):
    """Returns all inventory items with same given by a specific donor."""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select item_id, submitDate, description, status, amount, units, `type` from inventory
    where status = %s''', [status])
    return curs.fetchall()


def getInventoryByType(conn, itemType):
    """Returns all donations of a specific type."""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select item_id, submitDate, description, status, amount, units, `type` from inventory
    where `type` = %s''', [itemType])
    return curs.fetchall()


def setStatusforInventory(conn, item_id):
    '''Updates status for an item based on pre-defined values in setStatus table'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    
    
    itemAmountDictionary = curs.execute('''select amount
    from inventory where item_id = %s''', [item_id])
    itemAmount = curs.fetchall()[0]['amount'] #extracts amount corresponding to item

    thresholdForItem = curs.execute('''select thresholdLow, thresholdHigh
    from setStatus where item_id = %s''', [item_id])
    
    boththresholds = curs.fetchall()[0] #extracts dictionary containing thresholdHigh and threshLow
    thresholdLow = boththresholds['thresholdLow'] #extracts threshLow value for item
    thresholdHigh = boththresholds['thresholdHigh'] #extracts threshHigh value for item
    
    #set status depending on amount of item 
    if itemAmount <= thresholdLow:
        curs.execute('''update inventory set status = %s where item_id = %s''',
        ['low', item_id])
    elif itemAmount >= thresholdHigh:
        curs.execute('''update inventory set status = %s where item_id = %s''',
        ['high', item_id])
  



if __name__ == '__main__':
    conn = getConn('c9')
    allInventory = getAllInventoryHistoryInfo(conn) 
    print allInventory
