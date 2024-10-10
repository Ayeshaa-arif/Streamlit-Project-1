import mysql.connector 
import streamlit as st



#connection 

conn=mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",
    database="infographic_db"
)

c=conn.cursor()

#fetch

def view_all_data():
    c.execute('SELECT * FROM historical_data ORDER BY date ASC')
    data = c.fetchall()
    return data