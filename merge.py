# Initialise project
import streamlit as st
import pandas as pd
import numpy as np

def main():
    # Start Front End interface
    st.set_page_config(page_title='ODK Repeat Merger', page_icon="💙")

    st.title('Excel Sheet Selector')

    uploaded_file = st.file_uploader('Upload your xlsx file', type=['xlsx'])

    if uploaded_file is not None:
        try:
            # Load the Excel file
            excel_data = pd.read_excel(uploaded_file, sheet_name=None)

            # Get sheet names
            sheet_names = list(excel_data.keys())

            # Check if there is at least one sheet
            if len(sheet_names) < 1:
                st.error('Please upload an Excel file with at least one sheet.')
                return

            # Let the user choose the 'inner' and 'outer' sheets
            col1, col2 = st.columns(2)
            with col1:
                inner_sheet = st.selectbox('Choose the inner sheet:', sheet_names)
                dfinner = excel_data[inner_sheet]
                if not dfinner.empty:
                    inner_identifier_col = st.selectbox('Choose the common identifier column in this inner sheet:', dfinner.columns)
            with col2:
                outer_sheet = st.selectbox('Choose the outer sheet:', [name for name in sheet_names if name != inner_sheet])
                dfouter = excel_data[outer_sheet]
                if not dfouter.empty:
                    outer_identifier_col = st.selectbox('Choose the common identifier column in this outer sheet:', dfouter.columns)

            if not dfinner.empty and not dfouter.empty and inner_identifier_col and outer_identifier_col:
                merged_df = pd.merge(dfinner, dfouter, left_on=inner_identifier_col, right_on=outer_identifier_col, how='left')
                st.write('Merged DataFrame:')
                st.write(merged_df.head())


            # Display dataframes in the app
            st.write('Inner sheet (dfinner):', inner_sheet)
            st.write(dfinner.head())
            st.write('Outer sheet (dfouter):', outer_sheet)
            st.write(dfouter.head())

        except Exception as e:
            st.error(f"Error loading Excel file: {e}")

if __name__ == '__main__':
    main()
