import pandas as pd


def analyze_bias(df: pd.DataFrame):
    """
    Analyze dataset for potential bias and governance risks.
    Returns a dictionary with findings.
    """

    results = {}

    # 1️⃣ Missing values analysis
    missing = df.isnull().sum()
    results["missing_values"] = missing.to_dict()

    # 2️⃣ Detect categorical columns
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
    results["categorical_columns"] = categorical_cols

    imbalance_report = {}

    # 3️⃣ For each categorical column, check imbalance
    for col in categorical_cols:
        counts = df[col].value_counts(normalize=True)
        imbalance_report[col] = counts.to_dict()

    results["class_imbalance"] = imbalance_report

    # 4️⃣ Simple bias flag (if one group > 70%)
    bias_flags = {}
    for col, dist in imbalance_report.items():
        for group, pct in dist.items():
            if pct > 0.70:
                bias_flags[col] = f"Potential bias: '{group}' represents {pct * 100:.1f}% of the column."

    results["bias_flags"] = bias_flags

    return results
