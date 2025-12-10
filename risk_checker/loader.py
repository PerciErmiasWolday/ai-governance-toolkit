import pandas as pd

def load_dataset(path: str):
    """
    Loads a CSV dataset and returns a pandas DataFrame.
    Also returns a simple summary for governance purposes.
    """

    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        return None, {"error": f"File not found: {path}"}
    except pd.errors.EmptyDataError:
        return None, {"error": f"Dataset is empty: {path}"}
    except Exception as e:
        return None, {"error": str(e)}

    # Create a summary
    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": df.isnull().sum().to_dict(),
        "column_types": df.dtypes.astype(str).to_dict()
    }

    return df, summary
