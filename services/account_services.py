from database.db import get_connection

def create_account(user_id, account_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO accounts (user_id, account_type)
        VALUES (?, ?)
        """,
        (user_id, account_type)
    )

    conn.commit()
    conn.close()