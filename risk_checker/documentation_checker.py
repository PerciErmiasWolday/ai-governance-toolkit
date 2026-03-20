import json
from typing import Dict, Any, List


# --------------------------------------------------------------------
# LOAD MODEL METADATA
# --------------------------------------------------------------------
from pathlib import Path

def load_model_meta(path_or_text: Any) -> Dict[str, Any]:
    """Load metadata from dict, JSON string, or a JSON file."""
    if isinstance(path_or_text, dict):
        return path_or_text

    if isinstance(path_or_text, Path):
        path_or_text = str(path_or_text)

    # JSON string
    if isinstance(path_or_text, str):
        try:
            return json.loads(path_or_text)
        except Exception:
            pass

    # File path
    try:
        with open(path_or_text, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise ValueError(f"Could not load metadata from input: {e}")


# --------------------------------------------------------------------
# CHECK REQUIRED FIELDS
# --------------------------------------------------------------------
def check_fields(meta: Dict[str, Any]) -> Dict[str, Any]:
    required_fields = [
        "purpose",
        "intended_use",
        "limitations",
        "dataset_description",
        "privacy_notes",
        "evaluation_metrics",
    ]

    missing = [f for f in required_fields if f not in meta or not meta.get(f)]
    present = len(required_fields) - len(missing)
    pct = (present / len(required_fields)) * 100

    return {
        "missing_fields": missing,
        "score": present,
        "total_fields": len(required_fields),
        "completeness_score": f"{pct:.1f}%"
    }

# --------------------------------------------------------------------
# APPLY RULES
# --------------------------------------------------------------------

def apply_policy_rules(meta: dict, rules: dict) -> list:
    if not rules:
        return []
    violations = []

    for field, cond in rules.items():
        value = meta.get(field, "")

        # REQUIRED
        if cond.get("required", False):
            if not value or not str(value).strip():
                violations.append({
                    "field": field,
                    "issue": "missing required field",
                    "severity": cond.get("severity", "low")
                })
                continue  # don't check more rules for missing field

        # MIN LENGTH
        if "min_length" in cond:
            if len(str(value)) < cond["min_length"]:
                violations.append({
                    "field": field,
                    "issue": f"value too short (< {cond['min_length']})",
                    "severity": cond.get("severity", "low")
                })

        # MUST INCLUDE
        if "must_include" in cond:
            txt = str(value).lower()
            for kw in cond["must_include"]:
                if kw.lower() not in txt:
                    violations.append({
                        "field": field,
                        "issue": f"must include keyword '{kw}'",
                        "severity": cond.get("severity", "low")
                    })

    return violations


# --------------------------------------------------------------------
# GOVERNANCE SCORE (FINAL)
# --------------------------------------------------------------------
def compute_governance_score(fields: Dict[str, Any], violations: List[Dict[str, str]]) -> dict:
    score = 100

    # Missing fields (-20 each)
    score -= len(fields["missing_fields"]) * 20

    # Violations weighted by severity
    for v in violations:
        sev = v["severity"]
        if sev == "high":
            score -= 40
        elif sev == "medium":
            score -= 20
        else:
            score -= 10

    score = max(score, 0)

    return {
        "final_score": score,
        "missing_fields": fields["missing_fields"],
        "total_fields": fields["total_fields"],
    }


# --------------------------------------------------------------------
# REPORT GENERATION
# --------------------------------------------------------------------
def generate_recommendations(missing_fields, violations):
    recs = []

    for f in missing_fields:
        recs.append(f"Add missing required field: **{f}**.")

    for v in violations:
        recs.append(
            f"[{v['severity'].upper()}] **{v['field']}** – {v['issue']}."
        )

    return recs


def report_section_docs(meta: dict, rules: dict) -> str:
    """Generate final markdown report (Phase B)."""

    fields = check_fields(meta)
    violations = apply_policy_rules(meta, rules)
    score_data = compute_governance_score(fields, violations)

    md = []
    md.append("# 📘 Documentation Quality Report\n")

    md.append(f"### **Governance Score:** {score_data['final_score']} / 100\n")

    # -------------------------
    # MISSING FIELDS
    # -------------------------
    if fields["missing_fields"]:
        md.append("## 🚫 Missing Fields")
        for f in fields["missing_fields"]:
            md.append(f"- **{f}**")
        md.append("")

    # -------------------------
    # VIOLATIONS
    # -------------------------
    if violations:
        md.append("## ⚠️ Policy Violations")
        for v in violations:
            md.append(f"- **{v['field']}** – {v['issue']} (severity: {v['severity']})")
        md.append("")

    # -------------------------
    # RECOMMENDATIONS
    # -------------------------
    recs = generate_recommendations(fields["missing_fields"], violations)
    md.append("## 🛠️ Recommendations")

    if recs:
        md.extend([f"- {r}" for r in recs])
    else:
        md.append("- No issues detected.")

    return "\n".join(md)
