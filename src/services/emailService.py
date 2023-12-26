from src.connection.mysqlConnection import connect_to_database
from src.models.Email import EmailAccount


def find_email_by_id(email_id):
    try:
        connect = connect_to_database()
        cursor = connect.cursor(dictionary=True)
        query = "SELECT * FROM emails where email_id = %s"
        cursor.execute(query, (email_id,))
        result = cursor.fetchone()
        cursor.close()
        connect.close()
        email = EmailAccount(email_id=result['email_id'],
                             first_name=result['first_name'],
                             last_name=result['last_name'],
                             email_address=result['email_address'],
                             password=result['password'],
                             create_date=result['create_date'])

        return email

    except Exception as e:
        raise ConnectionError("Could not connect to database") from e
