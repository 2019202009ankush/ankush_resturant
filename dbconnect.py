from flaskext.mysql import MySQL


def connection(app):
    mysql = MySQL()
    # MySQL configurations
    mysql.init_app(app)
    conn = mysql.connect()
    cursor = conn.cursor()
    return conn, cursor

