import csv
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from utils.db import mysql


def create_csv_file(user_id, filename):

    csv_data = export_transactions_csv(user_id)

    with open(filename, "w", newline="", encoding="utf-8") as file:

        for chunk in csv_data:
            file.write(chunk)


def create_pdf_file(user_id, filename):

    pdf_data = export_transactions_pdf(user_id)

    with open(filename, "wb") as file:
        file.write(pdf_data.getvalue())


def transaction_generator(rows):

    for row in rows:

        yield [
            row["transaction_id"],
            row["user_id"],
            row["category_id"],
            row["amount"],
            row["type"],
            row["description"] or "",
            row["transaction_date"]
        ]


def export_transactions_csv(user_id):

    cur = mysql.connection.cursor()

    query = """
        SELECT
            transaction_id,
            user_id,
            category_id,
            amount,
            type,
            description,
            transaction_date
        FROM transactions
        WHERE user_id = %s
        ORDER BY transaction_date
    """

    cur.execute(query, (user_id,))

    def generate():

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "transaction_id",
            "user_id",
            "category_id",
            "amount",
            "type",
            "description",
            "transaction_date"
        ])

        yield output.getvalue()

        output.seek(0)
        output.truncate(0)

        while True:

            rows = cur.fetchmany(100)

            if not rows:
                break

            for row in transaction_generator(rows):
                writer.writerow(row)

            yield output.getvalue()

            output.seek(0)
            output.truncate(0)

        cur.close()

    return generate()


def export_transactions_pdf(user_id):

    cur = mysql.connection.cursor()

    query = """
        SELECT
            transaction_id,
            amount,
            type,
            description,
            transaction_date
        FROM transactions
        WHERE user_id = %s
        ORDER BY transaction_date
    """

    cur.execute(query, (user_id,))

    rows = cur.fetchall()

    cur.close()

    output = io.BytesIO()

    document = SimpleDocTemplate(
        output,
        pagesize=A4
    )

    data = [
        [
            "ID",
            "Amount",
            "Type",
            "Description",
            "Date"
        ]
    ]

    for row in rows:

        data.append([
            row["transaction_id"],
            row["amount"],
            row["type"],
            row["description"] or "",
            row["transaction_date"]
        ])

    table = Table(data)

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ])
    )

    document.build([table])

    output.seek(0)

    return output