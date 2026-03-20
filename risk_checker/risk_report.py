

def compute_dataset_risk(bias_results, summary):
    """
    Compute a risk score (0–100) based on:
    - Missing values
    - Categorical imbalance
    - Bias flags
    """

    score = 0
    details = []

    # 1️⃣ Missing values risk
    missing_vals = summary.get("missing_values", {})
    missing_count = sum(1 for x in missing_vals.values() if x > 0)

    if missing_count > 0:
        score += 20
        details.append("Missing values detected in dataset.")

    # 2️⃣ Categorical imbalance
    imbalance_flags = bias_results.get("bias_flags", {})
    if len(imbalance_flags) > 0:
        score += 40
        details.append("Strong categorical imbalance found.")

    # 3️⃣ Small dataset penalty
    if summary.get("rows", 0) < 50:
        score += 10
        details.append("Dataset is very small (<50 rows).")

    # Normalize score
    if score > 100:
        score = 100

    # Translate score into label
    if score <= 20:
        label = "Low Risk"
    elif score <= 60:
        label = "Medium Risk"
    else:
        label = "High Risk"

    return {
        "risk_score": score,
        "risk_level": label,
        "details": details
    }
