import pandas as pd
from pathlib import Path


def extract_csv(file_path: str) -> pd.DataFrame:
    """
    Read a CSV file and return it as a pandas DataFrame.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(path)

    return df