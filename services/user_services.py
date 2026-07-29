import bcrypt
from database.db import get_connection

#Register User
def register_user(full_name, email, password):
    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (full_name, email, password_hash)
        VALUES (?, ?, ?)
        """,
        (full_name, email, password_hash)
    )

    conn.commit()
    conn.close()


#Login User   
def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password_hash FROM users WHERE email = ?",
        (email,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        stored_hash = result[0]

        if bcrypt.checkpw(
            password.encode(),
            stored_hash
        ):
            return True

    return False