import csv


def export_statement(transactions, filename):
    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Reference",
            "Transaction Type",
            "Amount (Rs)",
            "Transaction Date",
        ])

        for reference, transaction_type, amount, date in transactions:

            writer.writerow([
                reference,
                transaction_type,
                f"{amount:.2f}",
                date,
            ])