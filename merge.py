import streamlit as st
import pandas as pd
import base64
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

def main():
    st.title('File Selector')


    # Upload either an Excel file or multiple CSV files
    uploaded_files = st.file_uploader('Upload your Excel or CSV files', type=['xlsx', 'csv'], accept_multiple_files=True)

    if uploaded_files:
        try:
            dataframes = {}

            # Check if the uploaded files are Excel or CSV
            if uploaded_files[0].type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                if len(uploaded_files) != 1:
                    st.error('Please upload only one Excel file.')
                else:
                    excel_file = pd.read_excel(uploaded_files[0], sheet_name=None)
                    dataframes = {f"Sheet {name}": df for name, df in excel_file.items()}
            else:
                dataframes = {f.name: pd.read_csv(f) for f in uploaded_files}

            # Let the user choose the 'inner' and 'outer' dataframes
            file_names = list(dataframes.keys())
            inner_file = st.selectbox('Choose the inner file or sheet:', file_names)
            outer_file = st.selectbox('Choose the outer file or sheet:', [name for name in file_names if name != inner_file])

            # Assign dfinner and dfouter based on user selection
            dfinner = dataframes[inner_file]
            dfouter = dataframes[outer_file]

            if not dfinner.empty and not dfouter.empty:
                inner_identifier_col = st.selectbox('Choose the common identifier column in the inner file or sheet:', dfinner.columns)
                outer_identifier_col = st.selectbox('Choose the common identifier column in the outer file or sheet:', dfouter.columns)

                if inner_identifier_col and outer_identifier_col:
                    merged_df = pd.merge(dfinner, dfouter, left_on=inner_identifier_col, right_on=outer_identifier_col, how='left')

                    st.write('Merged Dataset:')
                    st.dataframe(merged_df)
                    st.markdown(dataframe_to_csv_download_link(merged_df), unsafe_allow_html=True)
                    st.markdown(dataframes_to_excel_download_link([dfouter, dfinner, merged_df], ["outer", "inner", "merged"]), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error loading files: {e}")

if __name__ == '__main__':
    main()
