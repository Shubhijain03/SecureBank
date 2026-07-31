from database.db import get_connection


def get_admin_dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    # Total Users
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    # Total Accounts
    cursor.execute("SELECT COUNT(*) FROM accounts")
    total_accounts = cursor.fetchone()[0]

    # Total Transactions
    cursor.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = cursor.fetchone()[0]

    # Total Money in Bank
    cursor.execute("SELECT SUM(balance) FROM accounts")
    total_balance = cursor.fetchone()[0]

    conn.close()

    if total_balance is None:
        total_balance = 0

    return (
        total_users,
        total_accounts,
        total_transactions,
        total_balance
    )