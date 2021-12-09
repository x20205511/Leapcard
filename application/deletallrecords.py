import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# delete all rows from table
c.execute('DELETE FROM card;',);

print('We have deleted', c.rowcount, 'records from the table.')

#commit the changes to db			
conn.commit()
#close the connection
conn.close()