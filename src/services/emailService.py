import requests
import random
from src.connection.mysqlConnection import connect_to_database
from src.models.Email import EmailAccount
from src.services.deviceService import find_device_by_id
from src.utils.randomGenerate import generate_random_digit_string, generate_random_password


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
        if result['device_id']:
            device = find_device_by_id(result['device_id'])
            email.device = device
        return email

    except Exception as e:
        raise ConnectionError("Could not connect to database") from e


def get_all_emails(user_id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM emails where user_id = %s and is_deleted = False"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        emails = {}
        for row in result:
            emails[row['email_id']] = EmailAccount(email_id=row['email_id'],
                                                   first_name=row['first_name'],
                                                   last_name=row['last_name'],
                                                   device=find_device_by_id(row['device_id']),
                                                   email_address=row['email_address'],
                                                   password=row['password'],
                                                   create_date=row['create_date'],
                                                   status=row['status'],
                                                   is_deleted=bool(row['is_deleted']),
                                                   facebook=bool(row['facebook']),
                                                   tiktok=bool(row['tiktok']),
                                                   telegram=bool(row['telegram'])
                                                   )

        return emails

    except Exception as e:
        raise ConnectionError("Could not connect to database") from e


def remove_email(email_id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        alter_query = "UPDATE emails SET is_deleted = 1 WHERE email_id = %s"
        cursor.execute(alter_query, (email_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    except Exception as e:
        raise ConnectionError("Could not connect to database") from e


def generate_email_info():
    response = requests.get("https://story-shack-cdn-v2.glitch.me/generators/username-generator?count=6")
    random_info = {}
    if response.status_code == 200:
        data = response.json()
        username = data['data'][0]['name']
        email = username + generate_random_digit_string() + "@gmail.com"
        random_info['email'] = email

    response = requests.get("https://story-shack-cdn-v2.glitch.me/generators/vietnamese-name-generator?count=5")
    if response.status_code == 200:
        data = response.json()
        gender = ['male', 'female']
        choose_gender = random.choice(gender)
        name = data['data'][0][choose_gender]
        name = name.split(' ')
        first_name = name[0]
        last_name = name[1] + " " + name[2]
        random_info['first_name'] = first_name
        random_info['last_name'] = last_name
    random_info['password'] = generate_random_password()
    return random_info


def get_email_for_facebook(user_id):
    email_list = get_all_emails(user_id)
    for key in list(email_list.keys()):
        if email_list[key].facebook or email_list[key].is_deleted:
            del email_list[key]
    return email_list
