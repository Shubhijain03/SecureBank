from database.db import get_connection
from services.audit_services import log_action

from utils.display import (
    warning,
   )



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

    account_id = cursor.lastrowid

    account_number = f"SB{100000 + account_id}"

    cursor.execute(
        """
        UPDATE accounts
        SET account_number = ?
        WHERE account_id = ?
        """,
        (account_number, account_id)
    )

    conn.commit()
    conn.close()

    log_action(
        user_id,
        "CREATE_ACCOUNT",
        f"Created {account_type} account ({account_number})"
    )

    return account_number


def get_user_accounts(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT account_id,
               account_number,
               account_type,
               balance,
               status
        FROM accounts
        WHERE user_id = ?
        """,
        (user_id,)
    )

    accounts = cursor.fetchall()

    conn.close()

    return accounts


def choose_account(user_id):
    accounts = get_user_accounts(user_id)

    if not accounts:
        warning("No accounts found.")
        return None

    print("\n" + "=" * 75)
    print("                      SELECT AN ACCOUNT")
    print("=" * 75)
    print(f"{'NO.':<5}{'ACCOUNT NO.':<18}{'TYPE':<15}{'STATUS':<12}{'BALANCE'}")
    print("-" * 75)

    for index, account in enumerate(accounts, start=1):
        print(
            f"{index:<5}{account[1]:<18}{account[2]:<15}{account[4]:<12}Rs {account[3]:.2f}"
        )

    print("=" * 75)

    try:
        choice = int(input("Choose account (Number): "))
        print()

        if choice < 1 or choice > len(accounts):
            print("Invalid account selection!")
            return None

    except ValueError:
        print("Please enter a valid number!")
        return None

    # Return internal account_id
    return accounts[choice - 1][0]

def deactivate_account(account_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE accounts
        SET status = 'INACTIVE'
        WHERE account_id = ?
        """,
        (account_id,)
    )

    conn.commit()
    conn.close()


def activate_account(account_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE accounts
        SET status = 'ACTIVE'
        WHERE account_id = ?
        """,
        (account_id,)
    )

    conn.commit()
    conn.close()
    
def get_account_status(account_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status
        FROM accounts
        WHERE account_id = ?
        """,
        (account_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result[0]

def get_account_id_from_number(account_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT account_id
        FROM accounts
        WHERE account_number = ?
        """,
        (account_number,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None

def get_active_accounts(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            account_id,
            account_number,
            account_type,
            balance,
            status
        FROM accounts
        WHERE user_id = ?
        AND status = 'ACTIVE'
        ORDER BY account_id
        """,
        (user_id,)
    )

    accounts = cursor.fetchall()

    conn.close()

    return accounts