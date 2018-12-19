#!/usr/bin/python2.7

"""
Backend functions for searching and updating the inventory
----------------------------------------------------------------
CS 304 - Databases 

"""

import sys
import MySQLdb
from connection import get_conn
                    
def countInventoryTotal(conn):
    """Returns the number of items in inventory"""
    curs = conn.cursor()
    curs.execute(
        '''select count(*) from inventory''')
    return curs.fetchone()[0]
    
def statusCount(conn, status):
    """Returns the number of items with a given status"""
    curs = conn.cursor()
    curs.execute(
        '''select count(*) from inventory where status = %s''',[status])
    return curs.fetchone()[0]
    
def listLowItems(conn):
    """Returns list of low status items"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select description from inventory where status = "low"''')
    tupleList = curs.fetchall()
    list = [dictionary['description'] for dictionary in tupleList]
    return '\n'.join(list)
    
def mostDonationTypes(conn):
    """Returns list of types with the most donations aka items of high status"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select distinct type from inventory where status = "high"''')
    tupleList = curs.fetchall()
    list = [dictionary['type'] for dictionary in tupleList]
    return '\n'.join(list)


def getAllInventoryHistoryInfo(conn):
    """Returns all inventory, in order of last modified.
    since there could be none of an item, but then more added, 
    so updates should be first"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select description, inventory.item_id, units, amount, status, `type`, threshold from 
    inventory, setStatus where inventory.item_id = setStatus.item_id''')
    return curs.fetchall()
 

def combineFilters(conn, filter, sort):
    """Returns the inventory table after filtering and then sorting"""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    if (sort == "Status (Low to High)"):
        curs.execute(
        '''select item_id, description, status, amount, units, `type` from inventory
        where `type` = %s order by status desc''' ,[filter])
    else: # If sorting by type alphabetically    
        curs.execute(
            '''select item_id, description, status, amount, units, `type` from inventory
            where `type` = %s order by type''' ,[filter])
    return curs.fetchall() 
    
def sortInventoryType(conn):
    """Returns all inventory items alphabetically by type."""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select item_id, description, status, amount, units, `type` from inventory
        order by type''')
    return curs.fetchall()
    
def sortInventoryStatus(conn):
    """Returns all inventory items by status, low to high."""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
    '''select item_id, description, status, amount, units, `type` from inventory
        order by status desc''')
    return curs.fetchall()


def getInventoryItemTypes(conn):
    '''Returns all inventory types, used in update inventory form'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select description, item_id, units from inventory''')
    return curs.fetchall()


def getInventoryByType(conn, itemType):
    """Returns all donations of a specific type."""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select item_id, description, status, amount, units, `type` from inventory
    where `type` = %s''', [itemType])
    return curs.fetchall()


def addItemStatus(conn,item_id):
    ''' Adds a row to the setStatus table for the given item_id
        Threshold defaults to null'''
    curs = conn.cursor()
    curs.execute('''INSERT INTO setStatus(item_id) VALUES (%s)''', [item_id])
    
def getStatus(conn, item_id):
    '''checks if an item has status null'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select status
    from inventory where item_id = %s''', [item_id])
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
    print itemAmountDictionary
    itemAmount = curs.fetchall()[0]['amount'] #extracts amount corresponding to item

    thresholdForItemDictionary = curs.execute('''select threshold
    from setStatus where item_id = %s''', [item_id])
    
    result = curs.fetchall()
    if len(result) == 0:  #if item not found, result will be (), pass
        return
    
    thresholdForItem = result[0]['threshold']
    #set status depending on amount of item 
    if itemAmount <= thresholdForItem:
        setStatus(conn, item_id, 'low')
    else:
        setStatus(conn, item_id, 'high')
        
def updateInventory(conn, item_id, amount, threshold):
    '''updates the inventory table from the inventory form'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    
    #only updates if user entered an amount
    if amount != "":
        #updates inventory item with correct amount
        curs.execute('''update inventory set amount = %s where item_id = %s''', 
        [amount, item_id])
    
    #only updates if user entered a status
    if threshold != "":
        #updates threshold of item in setStatus table
        curs.execute('''update setStatus set threshold = %s where setStatus.item_id = %s''', 
        [threshold, item_id])
        
    #updates status in inventory table based on new amount
    updateStatus(conn, item_id)
    
        
    
if __name__ == '__main__':
    conn = get_conn()
    checking = getStatus(conn, 6)
    print (checking[0]['status'] == "null")
    