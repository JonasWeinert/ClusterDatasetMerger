import streamlit as st
import pandas as pd

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

            # Display dataframes in the app
            st.write('Inner file or sheet (dfinner):', inner_file)
            st.write(dfinner.head())
            st.write('Outer file or sheet (dfouter):', outer_file)
            st.write(dfouter.head())

            if not dfinner.empty and not dfouter.empty:
                inner_identifier_col = st.selectbox('Choose the common identifier column in the inner file or sheet:', dfinner.columns)
                outer_identifier_col = st.selectbox('Choose the common identifier column in the outer file or sheet:', dfouter.columns)

                if inner_identifier_col and outer_identifier_col:
                    merged_df = pd.merge(dfinner, dfouter, left_on=inner_identifier_col, right_on=outer_identifier_col, how='left')

                    st.write('Merged DataFrame:')
                    st.write(merged_df.head())

        except Exception as e:
            st.error(f"Error loading files: {e}")

if __name__ == '__main__':
    main()
