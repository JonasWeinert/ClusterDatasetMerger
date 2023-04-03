# file_processing.py

import pandas as pd
import streamlit_lottie as st_lottie
import requests

def read_files(uploaded_files):
    dataframes = {}

    if uploaded_files[0].type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        if len(uploaded_files) != 1:
            raise ValueError("Please upload only one Excel file.")
        else:
            excel_file = pd.read_excel(uploaded_files[0], sheet_name=None)
            dataframes = {f"Sheet {name}": df for name, df in excel_file.items()}
    else:
        dataframes = {f.name: pd.read_csv(f) for f in uploaded_files}

    return dataframes

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

