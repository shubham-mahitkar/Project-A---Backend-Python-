# Sql Query

# SQL_QUERY = '''
# CREATE TABLE `tbl_user` (
#   `user_id` bigint COLLATE utf8mb4_unicode_ci NOT NULL AUTO_INCREMENT,
#   `user_name` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#   `user_email` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#   `user_password` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#   PRIMARY KEY (`user_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;'''


from users.connectors.db import mysql
from users.utils import util
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:

    def __init__(self):
        # @todo try DictCursor instead of x[0]
        self.cursor = mysql.connection.cursor()

    def get_users(self):
        self.cursor.execute("SELECT user_id id, user_name name, user_email email, user_password password FROM tbl_user")
        data = self.cursor.fetchall()
        lst = []
        for x in data:
            # this would not be required with DictCursor
            inner_obj = {}
            inner_obj['id'] = x[0]
            inner_obj['name'] = x[1]
            inner_obj['email'] = x[2]
            inner_obj['password'] = x[3]
            lst.append(inner_obj)
        return lst

    def user_details(self, id):
        self.cursor.execute(f"SELECT user_id id, user_name name, user_email email, user_password password FROM tbl_user WHERE user_id={id}")
        user = self.cursor.fetchone()
        return user

    def add_user(self, name, email, password):
        sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
        data = (name, email, password)
        cursor = mysql.connection.cursor()
        cursor.execute(sql, data)
        mysql.connection.commit()
        return {"id":cursor.lastrowid, "name":name, "email": email, "password": password }

    def delete_user(self, id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
        mysql.connection.commit()

    def update_user(self, name, email, id):
        sql = "UPDATE tbl_user SET user_name=%s, user_email=%s WHERE user_id=%s"
        data = (name, email, id)
        cursor = mysql.connection.cursor()
        cursor.execute(sql, data)
        mysql.connection.commit()
        return {"id":id, "name":name, "email": email }

    def generate_and_hash_password(self):
        random_password = util.generate_random_password()
        hashed_password = generate_password_hash(random_password)
        return random_password, hashed_password

    def mysql_insert_bulk_users(self, csv_data):
        try:
            headers = next(csv_data)
            with mysql.connection.cursor() as cursor:
                for row in csv_data:
                    user_name, user_email = row[0], row[1]
                    random_password, hashed_password = self.generate_and_hash_password()

                    # Check if user with the same username or email already exists
                    select_sql = "SELECT COUNT(*) FROM tbl_user WHERE user_name = %s OR user_email = %s"
                    select_data = (user_name, user_email)
                    cursor.execute(select_sql, select_data)
                    result = cursor.fetchone()

                    if result[0] == 0:  # No existing user with the same username or email
                        # Insert the new user
                        insert_sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
                        insert_data = (user_name, user_email, hashed_password)

                        cursor.execute(insert_sql, insert_data)
                        mysql.connection.commit()
                    else:
                        print(f"User with username {user_name} or email {user_email} already exists.")
                        raise Exception(f"User with username {user_name} or email {user_email} already exists.")

        except Exception as e:
            print(e)


    def get_neo_id_by_name(self, name):
        self.cursor.execute(f"SELECT user_id id FROM tbl_user WHERE user_name='{name}'")
        neo_id = self.cursor.fetchone()
        return neo_id