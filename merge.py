import streamlit as st
import pandas as pd
from utils import dataframe_to_csv_download_link, dataframes_to_excel_download_link
from file_processing import read_files
import streamlit_lottie as st_lottie


lottie_loading_url = "https://assets6.lottiefiles.com/packages/lf20_keazd9nb.json"

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


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

                inner_col_dtype = dfinner[inner_identifier_col].dtype
                outer_col_dtype = dfouter[outer_identifier_col].dtype

                if inner_col_dtype == outer_col_dtype:
            
                    if inner_identifier_col and outer_identifier_col:
                        with st.spinner("Processing..."):
                            st_lottie.st_lottie(load_lottie_url(lottie_loading_url), speed=1, width=200, height=200)
                        # merged_df = pd.merge(dfinner, dfouter, left_on=inner_identifier_col, right_on=outer_identifier_col, how='left')
                            merged_df = pd.merge(dfinner, dfouter, left_on=inner_identifier_col, right_on=outer_identifier_col, how='left', indicator=True)

                            # count matches
                            num_matches = (merged_df['_merge'] == 'both').sum()
                            # error if no match
                            if num_matches == 0:
                                st.error('0 matches found based on the unique identifier.')
                            else:
                                st.success(f'{num_matches} matches made based on the unique identifier.')
                                st.write('Merged Dataset:')
                                st.dataframe(merged_df)
                                st.markdown(dataframe_to_csv_download_link(merged_df), unsafe_allow_html=True)
                                st.markdown(dataframes_to_excel_download_link([dfouter, dfinner, merged_df], ["outer", "inner", "merged"]), unsafe_allow_html=True)
                else:
                    st.error(f'0 matches found based on the unique identifier because they store different datatypes ({inner_col_dtype} & {outer_col_dtype}).')

        except Exception as e:
            st.error(f"Error loading files: {e}")

if __name__ == '__main__':
    merge()
