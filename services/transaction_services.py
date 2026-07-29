from database.db import get_connection


def deposit(account_id, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE accounts
        SET balance = balance + ?
        WHERE account_id = ?
        """,
        (amount, account_id)
    )

    cursor.execute(
        """
        INSERT INTO transactions
        (account_id, transaction_type, amount)
        VALUES (?, ?, ?)
        """,
        (account_id, "DEPOSIT", amount)
    )

    conn.commit()
    conn.close()
    
    
def withdraw(account_id, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE accounts
        SET balance = balance - ?
        WHERE account_id = ? AND balance >= ?
        """,
        (amount, account_id, amount)
    )

    if cursor.rowcount == 0:
        conn.close()
        return False

    cursor.execute(
        """
        INSERT INTO transactions
        (account_id, transaction_type, amount)
        VALUES (?, ?, ?)
        """,
        (account_id, "WITHDRAW", amount)
    )

    conn.commit()
    conn.close()

    return True

def get_transactions(account_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT transaction_type, amount, created_at
        FROM transactions
        WHERE account_id = ?
        ORDER BY created_at DESC
        """,
        (account_id,)
    )

    transactions = cursor.fetchall()

    conn.close()

    return transactions