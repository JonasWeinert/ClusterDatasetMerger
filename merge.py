import streamlit as st
import pandas as pd
from utils import dataframe_to_csv_download_link, dataframes_to_excel_download_link
from file_processing import read_files

def merge():
    st.title('File Selector')


    # Upload either an Excel file or multiple CSV files
    uploaded_files = st.file_uploader('Upload your Excel or CSV files', type=['xlsx', 'csv'], accept_multiple_files=True)

    if uploaded_files:
        try:
            dataframes = read_files(uploaded_files)

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
                    
                    # throw error if no matches found
                    if merged_df[outer_identifier_col].isna().all():
                            st.error('No matches found based on the unique identifiers.')
                    else:
                        st.write('Merged Dataset:')
                        st.dataframe(merged_df)
                        st.markdown(dataframe_to_csv_download_link(merged_df), unsafe_allow_html=True)
                        st.markdown(dataframes_to_excel_download_link([dfouter, dfinner, merged_df], ["outer", "inner", "merged"]), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error loading files: {e}")

if __name__ == '__main__':
    merge()
