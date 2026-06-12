from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from services.predictor import predict_scores

import io
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from openpyxl import Workbook   # ✅ NEW (Excel export)

app = Flask(__name__)

# ✅ Enable CORS for frontend (development-safe)
CORS(app, resources={r"/*": {"origins": "*"}})

# ===============================
# HOME ROUTE
# ===============================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "EcoPackAI backend running",
        "message": "Use POST /predict to get sustainability scores"
    })

# ===============================
# PREDICT ROUTE (UNCHANGED)
# ===============================
@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    result = predict_scores(data)
    return jsonify(result)

# ===============================
# PDF EXPORT (WORKING)
# ===============================
@app.route("/export/pdf", methods=["POST", "OPTIONS"])
def export_pdf():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 800, "EcoPackAI Sustainability Report")

    pdf.setFont("Helvetica", 12)
    y = 760

    for key, value in data.items():
        pdf.drawString(50, y, f"{key}: {value}")
        y -= 20

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="EcoPackAI_Sustainability_Report.pdf"
    )

# ===============================
# EXCEL EXPORT (FINAL & GUARANTEED)
# ===============================
@app.route("/export/xlsx", methods=["POST", "OPTIONS"])
def export_xlsx():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "EcoPackAI Report"

    # Header row
    ws.append(["Metric", "Value"])

    # Data rows
    for key, value in data.items():
        ws.append([key, value])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="EcoPackAI_Report.xlsx"
    )

# ===============================
# RUN SERVER
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
