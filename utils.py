# utils.py

import base64
import pandas as pd
import io

def dataframe_to_csv_download_link(df, filename="merged_dataframe.csv", link_name="Download CSV"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{link_name}</a>'
    return href

def dataframes_to_excel_download_link(dfs, sheet_names, filename="dataframes.xlsx", link_name="Download Excel"):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    for df, sheet_name in zip(dfs, sheet_names):
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    writer.save()
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">{link_name}</a>'
    return href
