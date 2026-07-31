from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def export_pdf(transactions, filename):
    document = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]
    heading_style.alignment = TA_CENTER

    normal_style = styles["BodyText"]

    elements = []

    # -------------------------------------------------
    # Title
    # -------------------------------------------------

    elements.append(Paragraph("SECUREBANK", title_style))
    elements.append(
        Paragraph(
            "Bank Account Statement",
            heading_style,
        )
    )

    elements.append(Spacer(1, 12))

    # -------------------------------------------------
    # Generated Date
    # -------------------------------------------------

    generated_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    elements.append(
        Paragraph(
            f"<b>Generated On:</b> {generated_date}",
            normal_style,
        )
    )

    elements.append(Spacer(1, 15))

    # -------------------------------------------------
    # Table
    # -------------------------------------------------

    data = [
        [
            "Reference",
            "Transaction Type",
            "Amount (Rs)",
            "Date",
        ]
    ]

    for reference, transaction_type, amount, date in transactions:

        data.append(
            [
                reference,
                transaction_type,
                f"{amount:.2f}",
                str(date),
            ]
        )

    table = Table(data)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("BOX", (0, 0), (-1, -1), 1.2, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ]
        )
    )

    elements.append(table)

    elements.append(Spacer(1, 20))

    # -------------------------------------------------
    # Summary
    # -------------------------------------------------

    elements.append(
        Paragraph(
            f"<b>Total Transactions:</b> {len(transactions)}",
            normal_style,
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            "This statement is computer generated.",
            normal_style,
        )
    )

    elements.append(
        Paragraph(
            "No signature is required.",
            normal_style,
        )
    )

    elements.append(Spacer(1, 20))

    # -------------------------------------------------
    # Footer
    # -------------------------------------------------

    footer_style = styles["BodyText"]
    footer_style.alignment = TA_CENTER

    elements.append(
        Paragraph(
            "SecureBank Banking Management System",
            footer_style,
        )
    )

    document.build(elements)