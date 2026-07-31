from utils.display import heading, info


def show_main_menu(
    is_admin=False,
    current_name=None,
):
    heading("\n" + "=" * 60)
    heading("                    SECUREBANK")
    heading("=" * 60)

    if current_name:
        info(f"Logged In : {current_name}")
    else:
        info("Logged In : Not Logged In")

    print("-" * 60)

    print("1. User Management")
    print("2. Account Management")
    print("3. Transactions")
    print("4. Reports")

    if is_admin:
        print("5. Admin Panel")
        print("6. Logout")
        print("7. Exit")
    else:
        print("5. Logout")
        print("6. Exit")

    print("-" * 60)

    return input("Enter choice: ")


def show_user_menu():
    heading("\n" + "=" * 60)
    heading("               USER MANAGEMENT")
    heading("=" * 60)

    print("1. Register")
    print("2. Login")
    print("3. Change Password")
    print("4. Back")

    print("-" * 60)

    return input("Enter choice: ")


def show_account_menu():
    heading("\n" + "=" * 60)
    heading("             ACCOUNT MANAGEMENT")
    heading("=" * 60)

    print("1. Create Account")
    print("2. View Accounts")
    print("3. Account Statistics")
    print("4. Account Status")
    print("5. Back")

    print("-" * 60)

    return input("Enter choice: ")


def show_view_accounts_menu():
    heading("\n" + "=" * 60)
    heading("                VIEW ACCOUNTS")
    heading("=" * 60)

    print("1. View All Accounts")
    print("2. View Active Accounts")
    print("3. Back")

    print("-" * 60)

    return input("Enter choice: ")


def show_account_status_menu():
    heading("\n" + "=" * 60)
    heading("               ACCOUNT STATUS")
    heading("=" * 60)

    print("1. Activate Account")
    print("2. Deactivate Account")
    print("3. Back")

    print("-" * 60)

    return input("Enter choice: ")


def show_transaction_menu():
    heading("\n" + "=" * 60)
    heading("                TRANSACTIONS")
    heading("=" * 60)

    print("1. Deposit")
    print("2. Withdraw")
    print("3. Transfer Money")
    print("4. View Transactions")
    print("5. Monthly Summary")
    print("6. Search Transactions")
    print("7. Bank Statement")
    print("8. Back")

    print("-" * 60)

    return input("Enter choice: ")


def show_search_transaction_menu():
    heading("\n" + "=" * 60)
    heading("           SEARCH TRANSACTIONS")
    heading("=" * 60)

    print("1. Deposit")
    print("2. Withdraw")
    print("3. Transfer")
    print("4. Receive")
    print("5. Back")

    print("-" * 60)

    return input("Enter choice: ")


def show_report_menu():
    heading("\n" + "=" * 60)
    heading("                  REPORTS")
    heading("=" * 60)

    print("1. Export CSV")
    print("2. Export PDF")
    print("3. View Audit Logs")
    print("4. Back")

    print("-" * 60)

    return input("Enter choice: ")


def show_admin_menu():
    heading("\n" + "=" * 60)
    heading("                ADMIN PANEL")
    heading("=" * 60)

    print("1. Dashboard")
    print("2. Back")

    print("-" * 60)

    return input("Enter choice: ")