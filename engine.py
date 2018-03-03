import csv
import pymysql

MYSQL_DATABASE_USER = "root"
MYSQL_DATABASE_PASSWORD = "Its%yD8zx"
MYSQL_DATABASE_DB = "Kaushik"
MYSQL_DATABASE_HOST = "localhost"



def connection():
    # Open database connection
    conn = pymysql.connect(MYSQL_DATABASE_HOST, MYSQL_DATABASE_USER, MYSQL_DATABASE_PASSWORD, MYSQL_DATABASE_DB)
    cursor = conn.cursor()
    return conn, cursor


def getData(user_id, show, pointer):

	conn, cursor = connection()
	cursor.execute('SELECT * FROM Dishes WHERE dish_type="{}";'.format(show))
	datas = cursor.fetchall()
	elements = []
	for data in datas:
		element = {}
		element['title'] = data[1] + "  ||  " + data[6] + "  ||  ₹ " + str(data[2])
		element['subtitle'] = data[5]
		element['image_url'] = data[3]
		buttons = []
		button1 = {
			"set_attributes": {
				"item_id": str(data[0]),
				"user_id": str(user_id)
			},
			"title": "Add to cart",
			"type": "show_block",
			"block_names": ["Ask quantity"]
		}
		buttons.append(button1)

		button2 = {
			"type": "show_block",
			"title": "Main Menu",
			"block_names": ["menu"]
		}
		buttons.append(button2)
		
		element["buttons"] = buttons
		elements.append(element)

	cursor.close()
	conn.close()
	return elements
