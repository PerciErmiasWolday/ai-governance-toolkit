import pandas as pd


def analyze_bias(df: pd.DataFrame):
    """
    Analyze dataset for potential bias and governance risks.
    Returns a dictionary with findings.
    """

    results = {}

    #  Missing values analysis
    missing = df.isnull().sum()
    results["missing_values"] = missing.to_dict()

    # Detect categorical columns
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
    results["categorical_columns"] = categorical_cols

    imbalance_report = {}

    #  For each categorical column, check imbalance
    for col in categorical_cols:
        counts = df[col].value_counts(normalize=True)
        imbalance_report[col] = counts.to_dict()

    results["class_imbalance"] = imbalance_report

    # Simple bias flag (if one group > 70%)
    bias_flags = {}
    for col, dist in imbalance_report.items():
        for group, pct in dist.items():
            if pct > 0.70:
                bias_flags[col] = f"Potential bias: '{group}' represents {pct * 100:.1f}% of the column."

    results["bias_flags"] = bias_flags

    return results
import matplotlib.pyplot as plt

def plot_imbalance(df, save_path="imbalance_plot.png"):
    """
    Plots category distribution for each categorical column.
    Saves the plot as a PNG file.
    """

    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    for col in categorical_cols:
        counts = df[col].value_counts()

        plt.figure(figsize=(6, 4))
        counts.plot(kind="bar", color="skyblue")

        plt.title(f"Category Distribution: {col}")
        plt.xlabel(col)
        plt.ylabel("Count")

        plt.tight_layout()

        # Save each chart separately
        file_name = f"{save_path.replace('.png', '')}_{col}.png"
        plt.savefig(file_name)
        plt.close()

    return "Plots saved successfully."
