from flask import Flask, render_template, request, send_file
import pandas as pd
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

from reportlab.pdfgen import canvas
from pathlib import Path

from risk_checker.bias_analysis import analyze_bias, plot_imbalance
from risk_checker.risk_report import compute_dataset_risk
from risk_checker.documentation_checker import check_fields


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dataset = request.files["dataset"]
        model_description = request.form["description"]

        # --- Paths / folders ---
        base_dir = Path(__file__).resolve().parent
        plots_dir = base_dir / "plots"
        plots_dir.mkdir(exist_ok=True)  # makes sure plots/ exists

        # Save uploaded dataset temporarily (inside project folder)
        dataset_path = base_dir / f"temp_{dataset.filename}"
        dataset.save(str(dataset_path))

        # Load dataset
        try:
            df = pd.read_csv(dataset_path)
        except UnicodeDecodeError:
            df = pd.read_csv(dataset_path, encoding='latin-1')
        # ===== 1) Hafsa: Bias analysis + charts =====
        bias_results = analyze_bias(df)
        # saves: plots/imbalance_<col>.png
        plot_imbalance(df, save_path=str(plots_dir / "imbalance"))
        chart_files = [
            plots_dir / "imbalance_sentiment.png",
            plots_dir / "imbalance_region.png",
            plots_dir / "imbalance_language.png",
        ]

        # Create summary dict (matches what the risk scorer expects)
        summary = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "missing_values": df.isnull().sum().to_dict(),
            "column_types": df.dtypes.astype(str).to_dict()
        }

        # ===== 2) Hafsa: Risk score =====
        risk_output = compute_dataset_risk(bias_results, summary)

        # ===== 3) Eya: Documentation check =====
        doc_path = base_dir / "model_doc.json"
        try:
            with open(doc_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            doc_report = check_fields(meta)  # <-- pass dict, not path
        except FileNotFoundError:
            doc_report = {"error": f"File not found: {doc_path}"}
        except json.JSONDecodeError:
            doc_report = {"error": f"Invalid JSON format: {doc_path}"}

        # ===== 4) Generate PDF report =====
        pdf_path = base_dir / "AI_Governance_Report.pdf"
        c = canvas.Canvas(str(pdf_path))

        y = 800
        c.drawString(50, y, "AI Governance Report"); y -= 30

        c.drawString(50, y, "Model Description:"); y -= 20
        # Split long text into lines so it doesn't go off the page
        for line in wrap_text(model_description, 90):
            c.drawString(70, y, line)
            y -= 15

        y -= 10
        c.drawString(50, y, f"Dataset Summary: {summary['rows']} rows, {summary['columns']} columns"); y -= 20

        # Risk score
        c.drawString(50, y, f"Dataset Risk Level: {risk_output['risk_level']}"); y -= 20
        c.drawString(50, y, f"Dataset Risk Score: {risk_output['risk_score']}"); y -= 20

        # Bias flags
        c.drawString(50, y, "Bias Flags:"); y -= 20
        if bias_results.get("bias_flags"):
            for col, msg in bias_results["bias_flags"].items():
                for line in wrap_text(f"- {col}: {msg}", 95):
                    c.drawString(70, y, line)
                    y -= 15
        else:
            c.drawString(70, y, "- None detected"); y -= 15

        y -= 10
        c.drawString(50, y, "Documentation Check:"); y -= 20
        if isinstance(doc_report, dict) and "error" in doc_report:
            c.drawString(70, y, f"- Error: {doc_report['error']}")
            y -= 15
        else:
            c.drawString(70, y, f"- Completeness: {doc_report.get('completeness_score', 'N/A')}")
            y -= 15
            missing = doc_report.get("missing_fields", [])
            missing_text = ", ".join(missing) if missing else "None"
            for line in wrap_text(f"- Missing fields: {missing_text}", 95):
                c.drawString(70, y, line)
                y -= 15

        y -= 10
        c.drawString(50, y, "Charts saved in /plots (imbalance_*.png)")
        # --- Add charts to PDF ---
        y -= 30
        c.drawString(50, y, "Charts:");
        y -= 20

        for chart_path in chart_files:
            if chart_path.exists():
                # If we're too low on the page, start a new page
                if y < 250:
                    c.showPage()
                    y = 750

                c.drawString(50, y, f"{chart_path.name}")
                y -= 15

                # Draw image (width/height tuned for page)
                img = ImageReader(str(chart_path))
                c.drawImage(img, 50, y - 180, width=500, height=180, preserveAspectRatio=True, mask='auto')
                y -= 200
            else:
                c.drawString(50, y, f"Missing chart: {chart_path.name}")
                y -= 20

        c.save()

        # Optional: cleanup temp file
        try:
            dataset_path.unlink()
        except Exception:
            pass

        return send_file(str(pdf_path), as_attachment=True)

    return render_template("index.html")


def wrap_text(text: str, width: int):
    """Simple word-wrap helper for PDF lines."""
    words = text.split()
    lines = []
    current = []
    for w in words:
        test = " ".join(current + [w])
        if len(test) <= width:
            current.append(w)
        else:
            lines.append(" ".join(current))
            current = [w]
    if current:
        lines.append(" ".join(current))
    return lines


if __name__ == "__main__":
    app.run(debug=True)
