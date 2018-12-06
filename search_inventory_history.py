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
                           user='cotequotey',
                           passwd='',
                           db=db)
                    
                           
def getAllInventoryHistoryInfo(conn, rowType='dictionary'):
    """Returns all inventory, in order of last modified.
    since there could be none of an item, but then more added, 
    so updates should be first"""
    if rowType == "tuple":
        curs = conn.cursor()
    elif rowType == "dictionary":
        # results as Dictionaries
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select item_id, description, status, relevance, `type` from inventory''')
    return curs.fetchall()
    
def getAllInventoryDescription(conn, rowType='dictionary'):
    """Returns all inventory, in order of last modified.
    since there could be none of an item, but then more added, 
    so updates should be first"""
    if rowType == "tuple":
        curs = conn.cursor()
    elif rowType == "dictionary":
        # results as Dictionaries
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        '''select item_id, description, status, relevance, `type` from inventory''')
    return curs.fetchall()
    
                               
def getInventoryByStatus(conn, status, rowType='dictionary'):
    """Returns all inventory items with same given by a specific donor."""
    if rowType == "tuple":
        curs = conn.cursor()
    elif rowType == "dictionary":
        # results as Dictionaries
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select item_id, description, status, relevance, `type` from inventory
    where status = %s''', [status])
    return curs.fetchall()


def getInventoryByType(conn, itemType):
    """Returns all donations of a specific type."""
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select item_id, description, status, relevance, `type` from inventory
    where `type` = %s''', [itemType])
    return curs.fetchall()
    
def getInventoryByRelevance(conn, relevance, rowType='dictionary'):
    """Returns all donations of a specific type."""
    if rowType == "tuple":
        curs = conn.cursor()
    elif rowType == "dictionary":
        # results as Dictionaries
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select item_id, description, status, relevance, `type` from inventory
    where status = %s''', [relevance])
    return curs.fetchall()



if __name__ == '__main__':
    conn = getConn('c9')
    allInventory = getAllInventoryHistoryInfo(conn) 
    print allInventory