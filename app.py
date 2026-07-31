from database.db import initialize_database

from cli.menu import (
    show_main_menu,
    show_user_menu,
    show_account_menu,
    show_account_status_menu,
    show_transaction_menu,
    show_report_menu,
    show_admin_menu,
    show_view_accounts_menu,
    show_search_transaction_menu, 
)

from utils.display import (
    heading,
    success,
    error,
    warning,
    info,
)

from services.admin_services import get_admin_dashboard

from services.audit_services import (
    get_audit_logs,
)

from services.user_services import (
    register_user,
    login_user,
    change_password,
)

from services.account_services import (
    create_account,
    get_user_accounts,
    choose_account,
    activate_account,
    deactivate_account,
    get_account_id_from_number,
    get_active_accounts,
)

from services.transaction_services import (
    deposit,
    withdraw,
    get_transactions,
    transfer_money,
    get_monthly_summary,
    search_transactions,
    get_account_statistics,
    get_statement_between_dates,
)

from utils.csv_export import export_statement
from utils.pdf_export import export_pdf


def main():
    initialize_database()
    print("\n" + "=" * 60)
    print("               WELCOME TO SECUREBANK")
    print("          Secure Banking Management System")
    print("=" * 60)

    current_user = None
    current_name = None
    is_admin = False

    while True:

        choice = show_main_menu(
            is_admin,
            current_name,
        )

        # =====================================================
        # USER MANAGEMENT
        # =====================================================

        if choice == "1":

            user_choice = show_user_menu()

            # ---------------- Register ----------------

            if user_choice == "1":

                name = input("Enter Name: ").strip()
                email = input("Enter Email: ").strip().lower()
                password = input("Enter Password: ").strip()

                if not name:
                    error("Name cannot be empty.")
                    continue

                if "@" not in email or "." not in email:
                    error("Enter a valid email address.")
                    continue

                if len(password) < 6:
                    error("Password must be at least 6 characters.")
                    continue

                result = register_user(
                    name,
                    email,
                    password,
                )

                if result:
                    heading( "=" * 60)
                    heading("Registration Successful!")
                    heading("=" * 60)
                    
                    print("Your account has been created.")
                    print("Please login to continue.")
                    print("=" * 60)
                else:
                    error(" An account with this email already exists.")

            # ---------------- Login ----------------

            elif user_choice == "2":
                email = input("Enter Email: ").strip().lower()
                password = input("Enter Password: ").strip()
                if not email or not password:
                    error("Email and Password are required.")
                    continue

                result = login_user(
                    email,
                    password,
                )

                if result:
                    current_user, current_name ,is_admin = result

                    print("\n" + "=" * 50)
                    success("Login successful.")
                    success(f"Welcome, {current_name}!")
                    print("=" * 50)

                else:
                    error(" Invalid email or password.")

            # ---------------- Change Password ----------------

            elif user_choice == "3":

                if current_user is None:
                    warning("Please login first!")
                    continue

                old_password = input("Enter current password: ")
                new_password = input("Enter new password: ")
                confirm_password = input("Confirm new password: ")

                if new_password != confirm_password:
                    error(" Passwords do not match.")
                    continue

                if len(new_password) < 6:
                    warning("Password must contain at least 6 characters.")
                    continue

                result = change_password(
                    current_user,
                    old_password,
                    new_password,
                )
                
                if result is True:
                    success("Password changed successfully.")

                elif result == "same_password":
                    warning("New password must be different from the current password.")

                else:
                    error("Current password is incorrect.")

            elif user_choice == "4":
                continue

            else:
                error("Invalid option.")

        # =====================================================
        # ACCOUNT MANAGEMENT
        # =====================================================

        elif choice == "2":

            if current_user is None:
                warning("Please login first!")
                continue

            account_choice = show_account_menu()

            # ---------------- Create Account ----------------

            if account_choice == "1":

                account_type = input(
                    "Enter Account Type (Savings/Current): "
                ).strip().title()

                if account_type not in ["Savings", "Current"]:
                    error("Invalid account type.")
                    continue

                account_number = create_account(
                    current_user,
                    account_type,
                )

                print("\n" + "=" * 60)
                success("Account created successfully.")
                info(f"Account Number : {account_number}")
                print("=" * 60)

            # ---------------- View Accounts ----------------

            elif account_choice == "2":

                option = show_view_accounts_menu()
                if option == "3":
                    continue

                if option == "1":
                    
                    accounts = get_user_accounts(current_user)

                elif option == "2":
                    accounts = get_active_accounts(current_user)

                else:
                    error("Invalid option.")
                    continue

                if not accounts:
                    warning("No accounts found.")
                    continue

                print("\n" + "=" * 70)
                print("                     YOUR ACCOUNTS")
                print("=" * 70)
                print(
                    f"{'ACCOUNT NUMBER':<20}"
                    f"{'TYPE':<15}"
                    f"{'STATUS':<12}"
                    f"{'BALANCE'}"
                )
                print("-" * 70)

                for account in accounts:

                    account_id = account[0]
                    account_number = account[1]
                    account_type = account[2]
                    balance = account[3]
                    status = account[4]

                    print(
                        f"{account_number:<20}"
                        f"{account_type:<15}"
                        f"{status:<12}"
                        f"Rs {balance:.2f}"
                    )

                print("=" * 70)

            # ---------------- Account Statistics ----------------

            elif account_choice == "3":

                account_id = choose_account(current_user)

                if account_id is None:
                    continue

                (
                    balance,
                    summary,
                    total_transactions,
                    last_transaction,
                ) = get_account_statistics(account_id)

                deposits = 0
                withdrawals = 0
                transfers = 0
                received = 0

                for transaction_type, count, total in summary:

                    if transaction_type == "DEPOSIT":
                        deposits = total

                    elif transaction_type == "WITHDRAW":
                        withdrawals = total

                    elif transaction_type == "TRANSFER":
                        transfers = total

                    elif transaction_type == "RECEIVE":
                        received = total

                heading("\n" + "=" * 60)
                heading("               ACCOUNT STATISTICS")
                heading("=" * 60)
                print(f"Current Balance      : Rs {balance:.2f}")
                print(f"Total Deposits       : Rs {deposits:.2f}")
                print(f"Total Withdrawals    : Rs {withdrawals:.2f}")
                print(f"Transfers Sent       : Rs {transfers:.2f}")
                print(f"Money Received       : Rs {received:.2f}")
                print(f"Total Transactions   : {total_transactions}")
                print(f"Last Transaction     : {last_transaction}")
                print("=" * 60)

            # ---------------- Activate / Deactivate ----------------

            elif account_choice == "4":
                account_id = choose_account(current_user)

                if account_id is None:
                    continue

                option = show_account_status_menu()

                if option == "1":
                    activate_account(account_id)
                    success(" Account activated successfully.")

                elif option == "2":
                    deactivate_account(account_id)
                    success("Account deactivated successfully.")

                elif option == "3":
                    continue

                else:
                    error("Invalid option.")

            # ---------------- Back ----------------

            elif account_choice == "5":

                continue

            else:

                error("Invalid option.")

        # =====================================================
        # TRANSACTIONS
        # =====================================================

        elif choice == "3":

            if current_user is None:
                warning("Please login first!")
                continue

            transaction_choice = show_transaction_menu()

            # -------------------------------------------------
            # Deposit
            # -------------------------------------------------

            if transaction_choice == "1":

                account_id = choose_account(current_user)

                if account_id is None:
                    continue

                try:
                    amount = float(input("Enter Amount (Rs): "))

                    if amount <= 0:
                        print("Amount must be greater than 0.")
                        continue

                except ValueError:
                    error("Invalid amount.")
                    continue

                deposit(
                    current_user,
                    account_id,
                    amount,
                )
                
                print( "=" * 50)
                success("Deposit Successful")
                print(f"Amount : Rs {amount:.2f}")
                print("=" * 50)

            # -------------------------------------------------
            # Withdraw
            # -------------------------------------------------

            elif transaction_choice == "2":

                account_id = choose_account(current_user)

                if account_id is None:
                    continue

                try:
                    amount = float(input("Enter Amount (Rs): "))

                    if amount <= 0:
                        print("Amount must be greater than 0.")
                        continue

                except ValueError:
                    error("Invalid amount.")
                    continue

                result = withdraw(
                    current_user,
                    account_id,
                    amount,
                )

                if result:
                    print("\n" + "=" * 50)
                    print("Withdrawal Successful")
                    print(f"Amount : Rs {amount:.2f}")
                    print("=" * 50)
                else:
                    error(" Insufficient balance.")

            # -------------------------------------------------
            # Transfer
            # -------------------------------------------------

            elif transaction_choice == "3":

                print("\nSelect Source Account")

                from_account = choose_account(current_user)

                if from_account is None:
                    continue

                account_number = input(
                    "Enter Destination Account Number: "
                ).strip()

                to_account = get_account_id_from_number(
                    account_number
                )
                
                if to_account == from_account:
                    error("Cannot transfer to the same account.")
                    continue

                if to_account is None:
                    print("Invalid Account Number.")
                    continue

                try:
                    amount = float(input("Enter amount: Rs "))

                    if amount <= 0:
                        print("Amount must be greater than 0.")
                        continue

                except ValueError:
                    error("Invalid amount.")
                    continue

                result = transfer_money(
                    current_user,
                    from_account,
                    to_account,
                    amount,
                )

                if result:
                    print("\n" + "=" * 50)
                    print("Transfer Successful")
                    print(f"Amount : Rs {amount:.2f}")
                    print("=" * 50)
                else:
                    error(" Transfer failed.")

            # -------------------------------------------------
            # View Transactions
            # -------------------------------------------------

            elif transaction_choice == "4":

                account_id = choose_account(current_user)

                if account_id is None:
                    continue

                transactions = get_transactions(account_id)

                if not transactions:
                    warning("No transactions found.")
                    continue

                heading("\n" + "=" * 85)
                heading("                    TRANSACTION HISTORY")
                heading("=" * 85)

                print(
                    f"{'REFERENCE':<18}"
                    f"{'TYPE':<15}"
                    f"{'AMOUNT':<15}"
                    f"{'DATE'}"
                )

                print("-" * 85)

                for reference, t_type, amount, date in transactions:

                    print(
                        f"{reference:<18}"
                        f"{t_type:<15}"
                        f"Rs {amount:<11.2f}"
                        f"{date}"
                    )

                print("=" * 85)

            # -------------------------------------------------
            # Monthly Summary
            # -------------------------------------------------

            elif transaction_choice == "5":

                account_id = choose_account(current_user)

                if account_id is None:
                    continue

                summary = get_monthly_summary(account_id)

                if not summary:
                    warning("No transactions found.")
                    continue

                heading("\n" + "=" * 70)
                heading("               MONTHLY SUMMARY")
                heading("=" * 70)

                total_transactions = 0

                print(
                    f"{'TYPE':<15}"
                    f"{'COUNT':<10}"
                    f"{'TOTAL'}"
                )

                print("-" * 70)

                for t_type, count, total in summary:

                    print(
                        f"{t_type:<15}"
                        f"{count:<10}"
                        f"Rs {total:.2f}"
                    )

                    total_transactions += count

                print("-" * 70)
                print(f"Total Transactions : {total_transactions}")
                print("=" * 70)

            # -------------------------------------------------
            # Search Transactions
            # -------------------------------------------------

            elif transaction_choice == "6":

                account_id = choose_account(current_user)

                if account_id is None:
                    continue

                option = show_search_transaction_menu()
                if option == "5":
                    continue

                mapping = {
                    "1": "DEPOSIT",
                    "2": "WITHDRAW",
                    "3": "TRANSFER",
                    "4": "RECEIVE",
                }

                if option not in mapping:
                    error("Invalid option.")
                    continue

                transactions = search_transactions(
                    account_id,
                    mapping[option],
                )

                if not transactions:
                    print("No matching transactions found.")
                    continue

                print("\n" + "=" * 75)

                print(
                    f"{'TYPE':<15}"
                    f"{'AMOUNT':<15}"
                    f"{'DATE'}"
                )

                print("-" * 75)

                for reference, t_type, amount, date in transactions:

                    print(
                       f"{reference:<18}"
                        f"{t_type:<15}"
                        f"Rs {amount:<11.2f}"
                        f"{date}"
                    )

                print("=" * 75)

            # -------------------------------------------------
            # Statement Between Dates
            # -------------------------------------------------

            elif transaction_choice == "7":

                account_id = choose_account(current_user)

                if account_id is None:
                    continue

                start = input("Start Date (YYYY-MM-DD): ").strip()
                end = input("End Date (YYYY-MM-DD): ").strip()

                transactions = get_statement_between_dates(
                    account_id,
                    start,
                    end,
                )

                if not transactions:
                    warning("No transactions found.")
                    continue
             
                heading("\n" + "=" * 85)
                heading("                  BANK STATEMENT")
                heading("=" * 85)

                print(f"From : {start}")
                print(f"To   : {end}")

                print("-" * 85)

                print(
                    f"{'REFERENCE':<18}"
                    f"{'TYPE':<15}"
                    f"{'AMOUNT':<15}"
                    f"{'DATE'}"
                )

                print("-" * 85)

                for reference, t_type, amount, date in transactions:

                    print(
                        f"{reference:<18}"
                        f"{t_type:<15}"
                        f"Rs {amount:<11.2f}"
                        f"{date}"
                    )

                print("=" * 85)

            elif transaction_choice == "8":
                continue

            else:
                error("Invalid option.")

        # =====================================================
        # REPORTS
        # =====================================================

        elif choice == "4":

            if current_user is None:
                warning("Please login first!")
                continue

            report_choice = show_report_menu()

            # ------------------------------------------
            # Export CSV
            # ------------------------------------------

            if report_choice == "1":

                account_id = choose_account(current_user)

                if account_id is None:
                    continue

                transactions = get_transactions(account_id)

                if not transactions:
                    warning("No transactions found.")
                    continue

                filename = f"exports/statement_account_{account_id}.csv"

                export_statement(
                    transactions,
                    filename,
                )
                print()

                print("\n" + "=" * 60)
                success("Statement exported successfully.")
                info(f"Saved As : {filename}")
                print("=" * 60)

            # ------------------------------------------
            # Export PDF
            # ------------------------------------------

            elif report_choice == "2":

                account_id = choose_account(current_user)

                if account_id is None:
                    continue

                transactions = get_transactions(account_id)

                if not transactions:
                    warning("No transactions found.")
                    continue

                filename = f"exports/statement_account_{account_id}.pdf"

                export_pdf(
                    transactions,
                    filename,
                )

                print("\n" + "=" * 60)
                success("PDF Statement Exported Successfully")
                info(f"Saved As : {filename}")
                print("=" * 60)

            # ------------------------------------------
            # Audit Logs
            # ------------------------------------------

            elif report_choice == "3":

                logs = get_audit_logs(current_user)

                if not logs:
                    print("No audit logs found.")
                    continue

                heading("\n" + "=" * 85)
                heading("                      AUDIT LOGS")
                heading("=" * 85)

                for action, description, created_at in logs:

                    print(f"Action      : {action}")
                    print(f"Description : {description}")
                    print(f"Date & Time : {created_at}")
                    print("-" * 85)

            # ------------------------------------------
            # Back
            # ------------------------------------------

            elif report_choice == "4":
                continue

            else:
                error("Invalid option.")

        # =====================================================
        # ADMIN PANEL
        # =====================================================

        elif choice == "5" and is_admin:

            admin_choice = show_admin_menu()

            # ------------------------------------------
            # Dashboard
            # ------------------------------------------

            if admin_choice == "1":

                (
                    total_users,
                    total_accounts,
                    total_transactions,
                    total_balance,
                ) = get_admin_dashboard()

                heading("\n" + "=" * 60)
                heading("                  ADMIN DASHBOARD")
                heading("=" * 60)
                
                print(f"Total Users         : {total_users}")
                print(f"Total Accounts      : {total_accounts}")
                print(f"Total Transactions  : {total_transactions}")
                print(f"Total Bank Balance  : Rs {total_balance:.2f}")
                print("=" * 60)

            # ------------------------------------------
            # Back
            # ------------------------------------------

            elif admin_choice == "2":
                continue

            else:
                error("Invalid option.")

        # =====================================================
        # LOGOUT
        # =====================================================

        elif (choice == "6" and is_admin) or (choice == "5" and not is_admin):

            if current_user is None:
                print("No user is currently logged in.")
            else:
                print("\n" + "=" * 50)
                print(f"Goodbye {current_name}")
                success("Logged out successfully.")
                print("=" * 50)

                current_user = None
                current_name = None
                is_admin = False

        # =====================================================
        # EXIT
        # =====================================================

        elif (choice == "7" and is_admin) or (choice == "6" and not is_admin):

            print("\n" + "=" * 60)
            print("Thank you for using SecureBank")
            print("Have a Great Day!")
            print("=" * 60)
            break

        else:
            error(" Invalid choice.")


if __name__ == "__main__":
    main()