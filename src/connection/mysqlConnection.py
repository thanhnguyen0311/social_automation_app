import mysql.connector

from src.constants.constants import account_data_config


def connect_to_database():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(user=account_data_config['user'],
                                             password=account_data_config['password'],
                                             host=account_data_config['host'],
                                             database=account_data_config['database'])

        if connection.is_connected():
            print('Connected to MySQL database')

            cursor = connection.cursor()

            cursor.execute('SELECT VERSION()')
            db_version = cursor.fetchone()
            print('MySQL Database Version:', db_version)
            return connection
    except mysql.connector.Error as err:
        print('Error:', err)

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if connection is not None:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
                print('Connection closed')
