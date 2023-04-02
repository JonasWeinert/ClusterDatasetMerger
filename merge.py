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

            if len(sheet_names) != 2:
                st.error('Please upload an Excel file with exactly two sheets.')
                return

            # Let the user choose which sheet is the 'inner sheet'
            inner_sheet = st.selectbox('Choose the inner sheet:', sheet_names)

            # Assign dfinner and dfouter based on user selection
            dfinner = excel_data[inner_sheet]
            dfouter = excel_data[sheet_names[1] if inner_sheet == sheet_names[0] else sheet_names[0]]

            # Display dataframes in the app
            st.write('Inner sheet (dfinner):', inner_sheet)
            st.write(dfinner.head())
            st.write('Outer sheet (dfouter):', sheet_names[1] if inner_sheet == sheet_names[0] else sheet_names[0])
            st.write(dfouter.head())

        except Exception as e:
            st.error(f"Error loading Excel file: {e}")

if __name__ == '__main__':
    main()
