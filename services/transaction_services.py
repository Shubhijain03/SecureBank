from database.db import get_connection
from services.audit_services import log_action
from services.account_services import get_account_status


def deposit(user_id, account_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    if get_account_status(account_id) != "ACTIVE":
        conn.close()
        return False

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
        (transaction_reference, account_id, transaction_type, amount)
        VALUES (?, ?, ?, ?)
        """,
        ("", account_id, "DEPOSIT", amount)
    )

    transaction_id = cursor.lastrowid
    reference = f"TXN{100000 + transaction_id}"

    cursor.execute(
        """
        UPDATE transactions
        SET transaction_reference = ?
        WHERE transaction_id = ?
        """,
        (reference, transaction_id)
    )

    conn.commit()
    conn.close()

    log_action(
        user_id,
        "DEPOSIT",
        f"Deposited Rs {amount:.2f} into Account {account_id}"
    )


def withdraw(user_id, account_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    
    if get_account_status(account_id) != "ACTIVE":
        conn.close()
        return False

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
        (transaction_reference, account_id, transaction_type, amount)
        VALUES (?, ?, ?, ?)
        """,
        ("", account_id, "WITHDRAW", amount)
    )

    transaction_id = cursor.lastrowid
    reference = f"TXN{100000 + transaction_id}"

    cursor.execute(
        """
        UPDATE transactions
        SET transaction_reference = ?
        WHERE transaction_id = ?
        """,
        (reference, transaction_id)
    )

    conn.commit()
    conn.close()

    log_action(
        user_id,
        "WITHDRAW",
        f"Withdrew Rs {amount:.2f} from Account {account_id}"
    )

    return True


def get_transactions(account_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            transaction_reference,
            transaction_type,
            amount,
            created_at
        FROM transactions
        WHERE account_id = ?
        ORDER BY created_at DESC
        """,
        (account_id,)
    )

    transactions = cursor.fetchall()

    conn.close()

    return transactions


def transfer_money(user_id, from_account_id, to_account_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    
    if get_account_status(from_account_id) != "ACTIVE":
        conn.close()
        return False

    if get_account_status(to_account_id) != "ACTIVE":
        conn.close()
        return False


    try:

        if from_account_id == to_account_id:
            conn.close()
            return False

        cursor.execute(
            "SELECT account_id FROM accounts WHERE account_id = ?",
            (to_account_id,)
        )

        if cursor.fetchone() is None:
            conn.close()
            return False

        cursor.execute(
            "SELECT balance FROM accounts WHERE account_id = ?",
            (from_account_id,)
        )

        result = cursor.fetchone()

        if result is None:
            conn.close()
            return False

        balance = result[0]

        if balance < amount:
            conn.close()
            return False

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance - ?
            WHERE account_id = ?
            """,
            (amount, from_account_id)
        )

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance + ?
            WHERE account_id = ?
            """,
            (amount, to_account_id)
        )

        cursor.execute(
            """
            INSERT INTO transactions
            (transaction_reference, account_id, transaction_type, amount)
            VALUES (?, ?, ?, ?)
            """,
            ("", from_account_id, "TRANSFER", amount)
        )

        transaction_id = cursor.lastrowid
        reference = f"TXN{100000 + transaction_id}"

        cursor.execute(
            """
            UPDATE transactions
            SET transaction_reference = ?
            WHERE transaction_id = ?
            """,
            (reference, transaction_id)
        )

        cursor.execute(
            """
            INSERT INTO transactions
            (transaction_reference, account_id, transaction_type, amount)
            VALUES (?, ?, ?, ?)
            """,
            ("", to_account_id, "RECEIVE", amount)
        )

        transaction_id = cursor.lastrowid
        reference = f"TXN{100000 + transaction_id}"

        cursor.execute(
            """
            UPDATE transactions
            SET transaction_reference = ?
            WHERE transaction_id = ?
            """,
            (reference, transaction_id)
        )

        conn.commit()

    except Exception:
        conn.rollback()
        conn.close()
        return False

    conn.close()

    log_action(
        user_id,
        "TRANSFER",
        f"Transferred Rs {amount:.2f} from Account {from_account_id} to Account {to_account_id}"
    )

    return True


def get_monthly_summary(account_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            transaction_type,
            COUNT(*),
            SUM(amount)
        FROM transactions
        WHERE account_id = ?
        GROUP BY transaction_type
        """,
        (account_id,)
    )

    summary = cursor.fetchall()

    conn.close()

    return summary


def search_transactions(account_id, transaction_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            transaction_reference,
            transaction_type,
            amount,
            created_at
        FROM transactions
        WHERE account_id = ?
        AND transaction_type = ?
        ORDER BY created_at DESC
        """,
        (account_id, transaction_type)
    )

    transactions = cursor.fetchall()

    conn.close()

    return transactions


def get_account_statistics(account_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT balance
        FROM accounts
        WHERE account_id = ?
        """,
        (account_id,)
    )

    balance = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT
            transaction_type,
            COUNT(*),
            COALESCE(SUM(amount),0)
        FROM transactions
        WHERE account_id = ?
        GROUP BY transaction_type
        """,
        (account_id,)
    )

    transaction_summary = cursor.fetchall()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE account_id = ?
        """,
        (account_id,)
    )

    total_transactions = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT created_at
        FROM transactions
        WHERE account_id = ?
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (account_id,)
    )

    last_transaction = cursor.fetchone()

    conn.close()

    return (
        balance,
        transaction_summary,
        total_transactions,
        last_transaction[0] if last_transaction else "No Transactions",
    )


def get_statement_between_dates(account_id, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            transaction_reference,
            transaction_type,
            amount,
            created_at
        FROM transactions
        WHERE account_id = ?
        AND DATE(created_at) BETWEEN DATE(?) AND DATE(?)
        ORDER BY created_at DESC
        """,
        (account_id, start_date, end_date)
    )

    transactions = cursor.fetchall()

    conn.close()

    return transactions