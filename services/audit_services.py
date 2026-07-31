from database.db import get_connection


def log_action(user_id, action, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO audit_logs
        (user_id, action, description)
        VALUES (?, ?, ?)
        """,
        (user_id, action, description)
    )

    conn.commit()
    conn.close()
    
def get_audit_logs(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            action,
            description,
            created_at
        FROM audit_logs
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    logs = cursor.fetchall()

    conn.close()

    return logs