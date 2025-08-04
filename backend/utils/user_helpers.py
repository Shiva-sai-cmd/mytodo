from extensions import mysql

def get_user_email_username(user_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT email, name FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    except Exception as e:
        print(f"❌ Error in get_user_email_username: {e}")
        return None
