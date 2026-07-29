from database.db import initialize_database
from services.transaction_services import deposit, withdraw, get_transactions


def main():
    initialize_database()

    deposit(1, 300)
    withdraw(1, 100)

    transactions = get_transactions(1)

    for transaction in transactions:
        print(transaction)


if __name__ == "__main__":
    main()