from extensions import mysql

def get_user_email_username(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT email, name FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result[0], result[1]  # email, name
    else:
        return None, None
