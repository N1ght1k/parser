import pymysql.cursors


def get_connection():
    connection = pymysql.connect(host='***',
                                 user='***',
                                 password='***',
                                 db='flight_schedule',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
