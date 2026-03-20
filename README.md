# AI Governance Toolkit

## Overview
The *AI Governance Toolkit* is a lightweight, Python-based system designed to support responsible AI development by identifying data risks, fairness concerns, and documentation gaps early in the AI lifecycle.

The toolkit provides automated checks for:
- Dataset quality and bias risks
- Model documentation completeness
- Governance rule compliance
- Interpretable risk and quality scoring
- Visual reporting for transparency

This project was developed as part of an internship to explore *practical AI governance, fairness, transparency, and accountability* principles.

---

## Key Features

### 1. Dataset Loading & Validation
- Safe loading of CSV datasets
- Automatic detection of:
  - Dataset shape (rows, columns)
  - Missing values
  - Data types
- Provides a structured dataset summary used across all governance checks

---

### 2. Bias & Fairness Analysis
- Identifies categorical features (e.g. gender, region, class)
- Analyzes category distributions
- Flags potential imbalance when one group dominates the data
- Generates bar chart visualizations for interpretability

This module focuses on *early-stage, distribution-based bias detection*, aligned with common governance screening practices.

---

### 3. Model Documentation Governance (Phase B)
A structured checker for evaluating AI model documentation stored in JSON format.

*Capabilities include:*
- Validation of required governance fields:
  - purpose
  - intended_use
  - limitations
  - dataset_description
  - privacy_notes
  - evaluation_metrics
- Detection of missing or incomplete sections
- Policy-based rule enforcement using configurable JSON rules
- Severity-aware violations (low / medium / high)
- Governance score computation
- Markdown and visual report generation

This ensures model documentation aligns with *baseline AI governance and transparency expectations*.

---

### 4. Governance Scoring & Visualization
- Aggregates documentation gaps and policy violations into a single governance score
- Generates visual summaries (charts) for:
  - Violations
  - Missing fields
  - Score interpretation
- Helps teams quickly understand governance readiness without manual review

---

## Project Structure
ai-governance-toolkit/
├── risk_checker/
│ ├── documentation_checker.py # Documentation governance logic
│ ├── bias_analysis.py # Bias & fairness checks
│ └── risk_report.py # Risk scoring logic
├── rules/
│ └── policies.json # Governance rules & severity levels
├── scripts/
│ ├── run_docs.py # CLI documentation checker
│ └── visual_report.py # Visualization report generator
├── samples/
│ └── sample_meta.json # Example model documentation
├── tests/
│ └── test_docs.py # Automated tests
├── plots/ # Generated charts
└── README.md


---

## How to Run (CLI)

### 1. Install Dependencies

pip install -r requirements.txt
2. Run Documentation Checker
python scripts/run_docs.py samples/sample_meta.json
3. Generate Visual Governance Report
python scripts/visual_report.py samples/sample_meta.json
This will output:

Governance score

Policy violations

Missing documentation fields

A generated visualization image

---
## Project Phases & Contributions

**Phase A – Dataset Handling & Bias Analysis**

-Contributor: **Hafsa**

Implemented dataset loading and validation

Designed distribution-based bias detection

Generated imbalance visualizations

Defined dataset risk levels and scoring logic

**Phase B – Documentation Governance**

-Contributor: **Eya**

Designed the model documentation checker

Defined required governance fields

Implemented policy-based rule checking with severity levels

Developed governance scoring logic

Generated structured documentation quality reports

Added visualization-based reporting for documentation governance

**Phase C – Application & Reporting**

-Contributor: **Perci**

Developed the Flask web application

Designed and styled the UI

Implemented PDF report generation

Integrated charts and governance results into final reports

Scope & Limitations
Bias analysis is currently distribution-based

No outcome-based or intersectional fairness analysis yet

Designed to avoid over-flagging and false positives

---

**Team**

Hafsa Outalb — Dataset governance, bias analysis, risk scoring

Eya Ben Amara — Documentation governance, policy rules, scoring

Perci — Web application, UI, reporting pipeline