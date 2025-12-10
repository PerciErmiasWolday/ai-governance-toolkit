import json

REQUIRED_FIELDS = [
    "model_name",
    "purpose",
    "dataset_description",
    "limitations",
    "evaluation_metrics",
    "intended_use",
    "not_intended_use",
    "privacy_and_security"
]

def check_documentation(doc_path):
    """
    Checks whether a model documentation JSON file has all required governance fields.
    Returns a report with missing fields and completeness score.
    """

    try:
        with open(doc_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"error": f"File not found: {doc_path}"}
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON format: {doc_path}"}
    except Exception as e:
        return {"error": str(e)}

    missing = []
    provided = []

    for field in REQUIRED_FIELDS:
        if field not in data or data[field] in ["", None]:
            missing.append(field)
        else:
            provided.append(field)

    completeness = len(provided) / len(REQUIRED_FIELDS) * 100

    report = {
        "provided_fields": provided,
        "missing_fields": missing,
        "completeness_score": f"{completeness:.1f}%"
    }

    return report
