# AI Governance Toolkit

A lightweight Python-based toolkit for assessing AI dataset risks, bias, and documentation completeness.  
This project is developed by Hafsa Outalb, Eya, and Perci as part of our internship experience.

## Features

### 1. Dataset Loader
- Safely loads CSV datasets
- Generates dataset summary (columns, rows, missing values, data types)

### 2. Bias & Fairness Checker
- Detects missing values
- Identifies categorical columns
- Computes imbalance in categories
- Flags potential governance risks (e.g., >70% dominance)

### 3. Model Documentation Checker
- Reads a JSON file describing a model
- Checks required governance fields
- Reports missing items
- Generates a completeness score

## Future Additions
- Risk scoring system
- Automated governance report generation
- Web interface

## How to Run

