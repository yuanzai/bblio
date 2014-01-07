import sqlite3 as lite
import sys


def getData():
    con = None

    try:
        con.row_factory = lite.Row    
        con = lite.connect('//mnt/my-data/db.sqlite3')
        cur = con.cursor()    
        cur.execute('SELECT * FROM doc')
        data = cur.fetchall()
    
    except lite.Error, e:
    
        print "Error %s:" % e.args[0]
        sys.exit(1)
    
    finally:
        if con:
            con.close()
        if data:
            return data
    
