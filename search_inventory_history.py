#!/usr/bin/python2.7

"""
Backend functions for searching and updating the inventory
----------------------------------------------------------------
CS 304 - Databases 

"""

import sys
import MySQLdb

                    
def countInventoryTotal(conn):
    """Returns the number of items in inventory"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select count(*) from inventory''')
    return curs.fetchall()[0]['count(*)']
    
def statusCount(conn, status):
    """Returns the number of items in inventory"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select count(*) from inventory where status = %s''',[status])
    return curs.fetchall()[0]['count(*)']
    
def getAllInventoryHistoryInfo(conn):
    """Returns all inventory, in order of last modified.
    since there could be none of an item, but then more added, 
    so updates should be first"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select item_id, submitDate, description, status, amount, units, `type` from inventory''')
    return curs.fetchall()

def combineFilters(conn, filter, sort):
    """Returns the inventory after filtering and then sorting"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select item_id, submitDate, description, status, amount, units, `type` from inventory
        where `type` = %s order by %s''' ,[filter,sort])
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

def setStatus(conn, item_id, newStatus):
    '''Sets status to newStatus, helper function for updateStatus'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''update inventory set status = %s where item_id = %s''',
        [newStatus, item_id])
    

def updateStatus(conn, item_id):
    '''Updates status for an item based on pre-defined values in setStatus table'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    
    itemAmountDictionary = curs.execute('''select amount
    from inventory where item_id = %s''', [item_id])
    print 'check!!!'
    itemAmount = curs.fetchall()[0]['amount'] #extracts amount corresponding to item

    thresholdForItemDictionary = curs.execute('''select threshold
    from setStatus where item_id = %s''', [item_id])
    
    thresholdForItem = curs.fetchall()[0]['threshold']
    
    #set status depending on amount of item 
    if itemAmount <= thresholdForItem:
        setStatus(conn, item_id, 'low')
    else:
        setStatus(conn, item_id, 'high')
        
def updateInventory(conn, item_id, amount):
    '''updates the inventory table from the inventory form'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    
    #updates inventory item with correct amount
    curs.execute('''update inventory set amount = %s where item_id = %s''', 
    [amount, item_id])
    
    #updates status based on new amount
    updateStatus(conn, item_id)
    
        
    
if __name__ == '__main__':
    conn = getConn('c9')