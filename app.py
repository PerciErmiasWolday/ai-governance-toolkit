from pathlib import Path
from risk_checker.loader import load_dataset
from risk_checker.bias_analysis import analyze_bias

# Base folder of the project
BASE_DIR = Path(__file__).resolve().parent

if __name__ == "__main__":
    csv_path = BASE_DIR / "data" / "example.csv"
    df, summary = load_dataset(csv_path)

    if df is None:
        print("Error:", summary["error"])
        exit()

    print("\n=== DATASET SUMMARY ===")
    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\n=== BIAS ANALYSIS ===")
    bias_results = analyze_bias(df)
    for key, value in bias_results.items():
        print(f"{key}: {value}")
from risk_checker.documentation_checker import check_documentation

print("\n=== DOCUMENTATION CHECK ===")
doc_report = check_documentation(BASE_DIR / "model_doc.json")

for key, value in doc_report.items():
    print(f"{key}: {value}")
