# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, request, json, url_for, flash, session, make_response

from flask import jsonify, json

import gc
from dbconnect import connection
from engine import getData

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Its%yD8zx'
app.config['MYSQL_DATABASE_DB'] = 'Kaushik'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


link = "http://139.59.30.59"



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/soup')
def show_soup():
    user_id = request.args.get("chatfuel user id")
    soup_pointer = request.args.get("soup")
    send = {
        "messages": [
            {
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "image_aspect_ratio": "square",
                    "elements": getData(user_id, show="SOUPS", pointer=soup_pointer)   
                }
            }
        }]
    }
    return jsonify(send)



@app.route('/starter')
def show_fruit():
    user_id = request.args.get("chatfuel user id")
    starter_pointer = request.args.get("starter")
    send = {
        "messages": [
            {
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "image_aspect_ratio": "square",
                    "elements": getData(user_id, show="STARTERS", pointer=starter_pointer)   
                }
            }
        }]
    }
    return jsonify(send)


@app.route('/maincourse')
def show_drink():
    user_id = request.args.get("chatfuel user id")
    maincourse_pointer = request.args.get("maincourse")
    send = {
        "messages": [
            {
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "image_aspect_ratio": "square",
                    "elements": getData(user_id, show="MAIN COURSE", pointer=maincourse_pointer)   
                }
            }
        }]
    }
    return jsonify(send)



def addToCart(data):
    conn, cursor = connection(app)
    try:
        # new order for user
        cursor.execute('SELECT id FROM Cart WHERE user_id="{}";'.format(data['user_id']))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO Cart (user_id, item_ordered, quantity) VALUES '
                           '("{0}", {1},  {2});'.format(data['user_id'], data['item'], data['quantity']))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            #
            cursor.execute('SELECT item_ordered, quantity FROM Cart WHERE user_id="{0}" '
                           'and item_ordered={1};'.format(data['user_id'], data['item']))
            result = cursor.fetchone()
            if result is not None:
                # modifying existing item
                cursor.execute(
                    'UPDATE Cart SET quantity = {0} WHERE user_id="{1}" '
                    'and item_ordered={2};'.format(data['quantity'], data['user_id'], data['item']))
                conn.commit()
                cursor.close()
                conn.close()
                return True
            else:
                # adding different item
                cursor.execute('INSERT INTO Cart (user_id, item_ordered, quantity) VALUES '
                               '("{0}", {1},  {2});'.format(data['user_id'], data['item'], data['quantity']))
                conn.commit()
                cursor.close()
                conn.close()
                return True
    except Exception as e:
        print(e)
        cursor.close()
        conn.close()
        return False


# /add_item/{{chatfuel user id}}/{{item_id}}/{{count}}
@app.route('/add_item/<user_id>/<int:item_id>/<int:quantity>', methods=['GET', 'POST'])
def order_received(user_id, item_id, quantity):
    data = {
        "user_id": user_id,
        "item": item_id,
        "quantity": quantity
    }
    if request.method == 'POST':
        if addToCart(data):
            price, name = get_price_and_name(int(item_id))
            send = {
                "messages": [
                    {
                        "text": str(name) + " x " + str(quantity)
                    },
                    {
                        "text": "Successfully Added"
                    },
                    {
                        "text": "Choose any one.",
                        "quick_replies": [
                            {
                                "title": "Cart 🛒",
                                "block_names": ["Cart"]
                            },
                            {
                                "title": "Main menu",
                                "block_names": ["menu"]
                            }
                        ]
                    }

                ]
            }

            return jsonify(send)
        else:
            return jsonify({
                "message": {
                    "text": "Item not Added."
                }
            })



@app.route('/update_item/<user_id>/<int:item_id>/<int:quantity>', methods=['GET', 'POST'])
def update_item(user_id, item_id, quantity):
    data = {
        "user_id": user_id,
        "item": item_id,
        "quantity": quantity
    }
    if request.method == 'GET':
        if addToCart(data):
            price, name = get_price_and_name(int(item_id))
            send = {
                "messages": [
                    {
                        "text": str(name) + " x " + str(quantity)
                    },
                    {
                        "text": "Successfully Added"
                    },
                    {
                        "text": "Choose any one.",
                        "quick_replies": [
                            {
                                "title": "Cart 🛒",
                                "block_names": ["Cart"]
                            },
                            {
                                "title": "Main menu",
                                "block_names": ["menu"]
                            }
                        ]
                    }

                ]
            }

            return jsonify(send)
        else:
            return jsonify({
                "message": {
                    "text": "Item not Added."
                }
            })



def get_price_and_name(dish_no):
    conn, cursor = connection(app)
    try:
        cursor.execute('SELECT dish_price, dish_name FROM Dishes WHERE dish_id={}'.format(dish_no))
        data = cursor.fetchone()
        return data[0], data[1]
    except Exception as e:
        print(e)
    finally:
        conn.close()
        cursor.close()


def count_quantity(item_no, user_id):
    conn, cursor = connection(app)
    try:
        cursor.execute('SELECT quantity FROM cart WHERE item_ordered={0} '
                       'and user_id="{1}"'.format(item_no, user_id))
        return cursor.fetchone()[0]
    except Exception as e:
        print(e)
    finally:
        conn.close()
        cursor.close()


@app.route("/show_cart/<user_id>", methods=['GET', 'POST'])
def show_cart(user_id):
    if request.method == 'GET':
        conn, cursor = connection(app)
        try:
            cursor.execute('SELECT * FROM Cart WHERE user_id="{}"'.format(user_id))
            data = cursor.fetchall()
            if len(data) == 0:
                send = {
                    "messages": [
                        {
                        "text": "There is nothing in your cart.",
                        "quick_replies": [
                            {
                                "title": "Main menu",
                                "block_names": ["menu"]
                            }]
                        }
                    ]
                }
                return jsonify(send)

            else:
                data = [i for i in data]
                print(len(data))
                total_price = 0
                elements = []
                details = ["You've added the following Items:"]
                for row in data:
                    price, name = get_price_and_name(int(row[2]))
                    total_price += row[3] * price
                    details.append(name + ": " + str(row[3]) + " Qty")

                details.append("Total Price: " + "₹ " + str(total_price))
                    
                print(details)
                send = {
                        "messages": [
                            {
                                "attachment": {
                                    "type": "template",
                                    "payload": {
                                        "template_type": "button",
                                        "text": '\n'.join(details),
                                        "buttons": [
                                        {
                                            "type": "show_block",
                                            "block_names": ["Confirm Order"],
                                            "title": "Confirm Order"
                                        },
                                        {
                                            "type": "json_plugin_url",
                                            "url": link + "/modify/" + user_id,
                                            "title": "Modify Order"
                                        },
                                        {
                                            "type": "show_block",
                                            "block_names": ["Cancel Order"],
                                            "title": "Cancel Order"
                                        }]
                                    }
                                }
                            }
                        ]
                }

                return jsonify(send)
        except Exception as e:
            print(e)
        finally:
            conn.close()
# 

def delete_quantity(user_id, item_ordered):
    conn, cursor = connection(app)
    try:
        cursor.execute('SELECT quantity FROM Cart WHERE '
                       'user_id="{0}" and item_ordered={1}'.format(user_id, item_ordered))
        data = cursor.fetchone()
        if data is not None:
                cursor.execute('DELETE FROM Cart WHERE user_id="{0}" '
                               'and item_ordered={1}'.format(user_id, item_ordered))
                conn.commit()
                return True
        else:
            return False
    except Exception as e:
        conn.close()
        cursor.close()


@app.route('/modify/<user_id>')
def modify(user_id):
    if request.method == 'GET':
        conn, cursor = connection(app)
        try:
            cursor.execute('SELECT * FROM Cart WHERE user_id="{}"'.format(user_id))
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            if len(data) == 0:
                print("1")
                send = {
                    "messages": [
                        {
                        "text": "There is nothing in your cart.",
                        "quick_replies": [
                            {
                                "title": "Main menu",
                                "block_names": ["menu"]
                            }]
                        }
                    ]
                }
                return jsonify(send)

            else:
                send = {
                    "messages": [
                        {
                            "text":  "What would you like to do?",
                            "quick_replies": [
                            {
                                "title":"Edit Item",
                                "url": "{}/pre_edit/{}".format(link, user_id),
                                "type":"json_plugin_url"
                            },
                            {
                                "title":"Delete Item",
                                "url": "{}/pre_delete/{}".format(link, user_id),
                                "type":"json_plugin_url"
                            }]
                        }
                    ]
                }
                return jsonify(send)
        except Exception as e:
            print(e)
            cursor.close()
            conn.close()


# =====================================================================
@app.route('/pre_edit/<user_id>')
def pre_edit(user_id):
    conn, cursor = connection(app)
    try:
        cursor.execute('SELECT * FROM Cart WHERE user_id="{}"'.format(user_id))
        data = cursor.fetchall()
        print(data)
        if len(data) == 0:
            print("1")
            send = {
                "messages": [
                    {
                        "text": "There is nothing in your cart.",
                        "quick_replies": [
                            {
                                "title": "Main menu",
                                "block_names": ["menu"]
                        }]
                    }
                ]
            }
            return jsonify(send)

        else:
            print("2")
            data = [i for i in data]
            print(len(data))
            total_price = 0
            elements = []
            for row in data:
                item_id = int(row[2])
                price, name = get_price_and_name(item_id)
                element = {
                    "title": "{}".format(name),
                    "url": "{}/edit_item/{}/{}".format(link, user_id, item_id),
                    "type": "json_plugin_url"
                }
                elements.append(element)

            send = {
                "messages": [
                    {
                        "text":  "Choose an item you wanna edit.",
                        "quick_replies": elements
                        }]
            }
            return jsonify(send)
    except Exception as e:
        print(e)
    send = {
        "messages": [
            {
                "text": "Modddiifffyyy Qty"
            }
        ]
    }
    return jsonify(send)


@app.route('/edit_item/<user_id>/<int:item_id>', methods=["GET"])
def edit_item(user_id, item_id):
    conn, cursor = connection(app)
    try:
        cursor.execute('SELECT * FROM Cart WHERE user_id="{}"'.format(user_id))
        data = cursor.fetchall()
        if data:
            elements = []
            for i in range(1, 8):
                element = {
                    "title": str(i),
                    "url": "{}/update_item/{}/{}/{}".format(link, user_id, item_id, i),
                    "type": "json_plugin_url"
                }
                elements.append(element)

            send = {
                "messages": [
                    {
                        "text":  "How many would you like to add?",
                        "quick_replies": elements
                    }
                ]
            }
            return jsonify(send)
        else:
            send = {
                "messages": [
                    {
                    "text": "There is nothing in your cart",
                    "quick_replies": [
                        {
                            "title": "Main menu",
                            "block_names": ["menu"]
                    }]
                    }
                ]
            }
            return jsonify(send)
    except Exception as e:
        print(e)
        cursor.close()
        conn.close()
    send = {
        "messages": [
            {
            "text": "Some Error Occured."
            }
        ]
    }
    return jsonify(send)
# =================================================


@app.route('/pre_delete/<user_id>')
def pre_delete(user_id):
    conn, cursor = connection(app)
    try:
        cursor.execute('SELECT * FROM Cart WHERE user_id="{}"'.format(user_id))
        data = cursor.fetchall()
        if len(data) == 0:
            send = {
                "messages": [
                    {
                        "text": "There is nothing in your cart.",
                        "quick_replies": [
                        {
                            "title": "Main menu",
                            "block_names": ["menu"]
                        }]
                    }
                ]
            }
            return jsonify(send)

        else:
            data = [i for i in data]
            total_price = 0
            elements = []
            for row in data:
                item_id = int(row[2])
                price, name = get_price_and_name(item_id)
                element = {
                    "title": "{}".format(name),
                    "url": "{}/delete_item/{}/{}".format(link, user_id, item_id),
                    "type": "json_plugin_url"
                }
                elements.append(element)

            send = {
                "messages": [
                    {
                        "text":  "Choose an item you wanna delete from your cart.",
                        "quick_replies": elements
                        }]
            }
            return jsonify(send)
    except Exception as e:
        print(e)
    send = {
        "messages": [
            {
                "text": "Modify Qty"
            }
        ]
    }
    return jsonify(send)






@app.route('/delete_item/<user_id>/<int:item_id>', methods=["GET"])
def delete_item(user_id, item_id):
    if request.method == 'GET':
        if delete_quantity(user_id, item_id):
            send = {
                    "messages": [
                        {
                        "text": "Item is removed from your cart.",
                        "quick_replies": [
                            {
                                "title":"Cart",
                                "block_names": ["Cart"]
                            },
                            {
                                "title":"Main menu",
                                "block_names": ["menu"]
                            }]
                        }
                    ]
            }
            return jsonify(send)
        else:
            send = {
                "messages": [
                    {"text": "This is item not present in your cart."}
                ]
            }
            return jsonify(send)
    else:
        return None

# =============================================================



@app.route('/cancel_order', methods=["GET"])
def cancel_order():
    print("1")
    print(request.method)
    if request.method == "GET":
        user_id = request.args['chatfuel user id']
        print(user_id)
        conn, cursor = connection(app)
        try:
            print("2")
            cursor.execute('DELETE FROM Cart WHERE user_id = {}'.format(user_id))
            conn.commit()
            send = {
                "messages": [
                    {
                    "text": "All the items from your cart has been deleted",
                    "quick_replies": [
                        {
                            "title": "Main menu",
                            "block_names": ["menu"]
                        },
                        {
                            "title": "Soup",
                            "type": "json_plugin_url",
                            "url": "{}/soup".format(link)
                        },
                        {
                            "title": "Starter",
                            "type": "json_plugin_url",
                            "url": "{}/starter".format(link)
                        },
                        {
                            "title": "Main course",
                            "type": "json_plugin_url",
                            "url": "{}/maincourse".format(link)
                        }]
                }]
            }
            cursor.close()
            conn.close()
            return jsonify(send)
        except Exception as e:
            print(e)



@app.route('/clear_order', methods=["GET"])
def clear_order():
    print("1")
    print(request.method)
    if request.method == "GET":
        user_id = request.args['chatfuel user id']
        print(user_id)
        conn, cursor = connection(app)
        try:
            print("2")
            cursor.execute('DELETE FROM Cart WHERE user_id = {}'.format(user_id))
            conn.commit()
            send = {
                "messages": [
                ]
            }
            cursor.close()
            conn.close()
            return jsonify(send)
        except Exception as e:
            print(e)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RV'
if __name__ == "__main__":
    app.run(port=5000)
