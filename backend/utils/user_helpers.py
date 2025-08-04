from extensions import mysql

def get_user_email_username(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name, email FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result[1], result[0]  
    else:
        return None, None
