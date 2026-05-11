import os
from datetime import datetime


def save_raw_file(uploaded_file, prefix):
    """
    Save uploaded CSV files to data/raw.
    """

    os.makedirs("data/raw", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"data/raw/{prefix}_{timestamp}.csv"

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path