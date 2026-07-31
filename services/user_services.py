import bcrypt
from database.db import get_connection
import sqlite3
from services.audit_services import log_action

#Register User
def register_user(full_name, email, password):
    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (full_name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (full_name, email, password_hash)
        )

        conn.commit()
        cursor.execute(
            "SELECT user_id FROM users WHERE email = ?",
            (email,)
        )

        user_id = cursor.fetchone()[0]

        log_action(
            user_id,
            "REGISTER",
            "User registered successfully."
        )
               
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


#Login User   
def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user_id, full_name, password_hash, is_admin
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        user_id = result[0]
        full_name = result[1]
        stored_hash = result[2]
        is_admin = result[3]

        if bcrypt.checkpw(
            password.encode(),
            stored_hash
        ):
            log_action(
                user_id,
                "LOGIN",
                "User logged in successfully."
            )

            return (
                user_id,
                full_name,
                is_admin,
            )

    return None

def make_admin(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET is_admin = 1
        WHERE email = ?
        """,
        (email,)
    )

    conn.commit()
    conn.close()
    
    
def change_password(user_id, old_password, new_password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT password_hash
        FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    )

    result = cursor.fetchone()

    if result is None:
        conn.close()
        return False

    stored_hash = result[0]

    if not bcrypt.checkpw(old_password.encode(), stored_hash):
        conn.close()
        return False
    
    if bcrypt.checkpw(new_password.encode(), stored_hash):
        conn.close()
        return "same_password"

    new_hash = bcrypt.hashpw(
        new_password.encode(),
        bcrypt.gensalt()
    )

    cursor.execute(
        """
        UPDATE users
        SET password_hash = ?
        WHERE user_id = ?
        """,
        (new_hash, user_id)
    )

    conn.commit()
    conn.close()

    return True