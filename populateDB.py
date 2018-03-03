#!/usr/bin/python
# -*- coding: latin-1 -*-



import csv
import pymysql

MYSQL_DATABASE_USER = "root"
MYSQL_DATABASE_PASSWORD = "Rahul@95"
MYSQL_DATABASE_DB = "Kaushik"
MYSQL_DATABASE_HOST = "localhost"






def connection():
    # Open database connection
    conn = pymysql.connect(MYSQL_DATABASE_HOST, MYSQL_DATABASE_USER, MYSQL_DATABASE_PASSWORD, MYSQL_DATABASE_DB, charset="utf8")
    cursor = conn.cursor()
    return conn, cursor


def insertdata():
	conn, cursor = connection()
	with open("Restaurant.csv", "r") as csvfile:
	    csv_reader = csv.DictReader(csvfile)
	    for row in csv_reader:
	        if row["dish_name"] == "":
	        	continue
	        print(row['dish_name'])
	        cursor.execute('INSERT INTO Dishes (dish_name, dish_price, dish_url, dish_type, dish_desc, dish_nature) VALUES ("{0}", {1}, "{2}", "{3}", "{4}", "{5}")'.format(row['dish_name'], row['dish_price'], row['dish_url'], row['dish_type'], row['dish_desc'], row['dish_nature']))
	        conn.commit()
	cursor.close()
	conn.close()
insertdata()



# INSERT INTO Dishes (dish_name, dish_price, dish_url, dish_type, dish_desc, dish_nature) VALUES ("")