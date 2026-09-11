from flask import Blueprint, session, send_file
from utils.decorators import login_required
from utils.export import create_csv_file, create_pdf_file


export_bp = Blueprint("export", __name__)


@export_bp.route("/export/csv", methods=["GET"])
@login_required
def export_csv():

    user_id = session["user_id"]
    filename = "transactions.csv"
    try:

        create_csv_file(user_id, filename)
        return send_file(
            filename,
            as_attachment=True,
            download_name="transactions.csv",
            mimetype="text/csv"
        )

    except Exception as e:

        print("CSV export error:", e)
        return {
            "error": "CSV export failed"
        }, 500


@export_bp.route("/export/pdf", methods=["GET"])
@login_required
def export_pdf():

    user_id = session["user_id"]
    filename = "transactions.pdf"
    try:

        create_pdf_file(user_id, filename)
        return send_file(
            filename,
            as_attachment=True,
            download_name="transactions.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        print("PDF export error:", e)
        return {
            "error": "PDF export failed"
        }, 500