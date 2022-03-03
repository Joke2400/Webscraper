from flask_sqlalchemy import SQLAlchemy



import sqlite3

con = sqlite3.connect("test_database.db") #":memory:" if memory only

c = con.cursor()

'''
c.execute("""CREATE TABLE employees (
    first text,
    last text,
    pay integer
    )""")
'''
#c.execute("INSERT INTO employees VALUES ('Joakim', 'Lohikoski', 55000)")

c.execute("SELECT * FROM employees WHERE last='Lohikoski'")

#c.fetchone()
#c.fetchmany(5)
print(c.fetchall())

con.commit()

con.close()

