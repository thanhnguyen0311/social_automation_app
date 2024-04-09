import requests

from src.connection.mysqlConnection import connect_to_database


def get_posts(PAGE_ID, PAGE_TOKEN):
    url = f'https://graph.facebook.com/v19.0/{PAGE_ID}/published_posts?access_token={PAGE_TOKEN}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            posts = data['data'][:10]
            post_ids = []
            for post in posts:
                post_ids.append(post['id'])
            return post_ids  # Assuming the API returns JSON data
        else:
            print("Failed to retrieve data from the API. Status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None


def check_new_posts(post_ids):
    new_post_id = []
    for post_id in post_ids:
        print(f"checking {post_id} ")
        try:
            connection = connect_to_database()
            cursor = connection.cursor(dictionary=True)
            select_query = "SELECT * FROM page_posts WHERE post_id = %s"
            cursor.execute(select_query, (post_id,))
            result = cursor.fetchone()
            if result:
                cursor.close()
                connection.close()
                continue
            else:
                insert_query = "INSERT INTO page_posts (post_id) VALUES (%s)"
                cursor.execute(insert_query, (post_id,))
                connection.commit()
                cursor.close()
                connection.close()
                new_post_id.append(post_id)
                continue

        except Exception as e:
            raise ConnectionError("Could not connect to database") from e

    return new_post_id
