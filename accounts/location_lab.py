import sqlite3

def labor_place(pincode):
    con = sqlite3.connect('/home/mehakpreet/ppcrc/testposition/prcatice/address.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT place FROM address WHERE pin_code = '{0}'".format(pincode))
    result=cur.fetchall()
    tup=result[0]
    location=tup[0]
    con.close()
    return location

