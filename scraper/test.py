import MySQLdb

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="", # your password
                      db="scrapedata")
cur = db.cursor()



cur.execute("SELECT * FROM doc")
for row in cur.fetchall():
   print row
