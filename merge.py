# Initialise project
import streamlit as st
import pandas as pd
import numpy as np

def main():
    # Start Front End interface
    st.set_page_config(page_title='ODK Repeat Merger', page_icon="💙")

    ################### Front End ###################
    # Set Front End appearance
    st.title('Hirarchical dataset merger') # Title
    st.markdown('This website produces a dingle dataset from two datasets of different levels.') # First paragraph
    st.subheader('Upload your datasets.') # Upload prompt
    uploaded_file = st.file_uploader('Either multiple csv files or single xlsx file with one sheet per dataset', type='xlsx', accept_multiple_files=True) # Save file to memory for duration of session

    if uploaded_file is not None:
        # Load the Excel file and get sheet names
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names

        # Check if there are exactly two sheets
        if len(sheet_names) != 2:
            st.error('Please upload an Excel file with exactly two sheets.')
            return

        # Let the user choose which sheet is the 'inner sheet'
        inner_sheet = st.selectbox('Choose the inner sheet:', sheet_names)

        # Read the sheets into dataframes
        df1 = pd.read_excel(excel_file, sheet_name=sheet_names[0])
        df2 = pd.read_excel(excel_file, sheet_name=sheet_names[1])

        # Assign dfinner and dfouter based on user selection
        if inner_sheet == sheet_names[0]:
            dfinner = df1
            dfouter = df2
        else:
            dfinner = df2
            dfouter = df1

        # Display dataframes in the app
        st.write('Inner sheet (dfinner):', inner_sheet)
        st.write(dfinner.head())
        st.write('Outer sheet (dfouter):', sheet_names[1] if inner_sheet == sheet_names[0] else sheet_names[0])
        st.write(dfouter.head())
# Start Front End interface
st.set_page_config(page_title='ODK Repeat Merger', page_icon="💙")

################### Front End ###################
# Set Front End appearance
st.title('Hirarchical dataset merger') # Title
st.markdown('This website produces a dingle dataset from two datasets of different levels..') # First paragraph
st.subheader('Upload your datasets.') # Upload prompt
uploaded_file = st.file_uploader('Either multiple csv files or single xlsx file with one sheet per dataset', type='xlsx', accept_multiple_files=True) # Save file to memory for duration of session

if uploaded_file is not None:
    # Load the Excel file and get sheet names
    excel_file = pd.ExcelFile(uploaded_file)
    sheet_names = excel_file.sheet_names

    # Check if there are exactly two sheets
    if len(sheet_names) != 2:
        st.error('Please upload an Excel file with exactly two sheets.')
        #return

    # Let the user choose which sheet is the 'inner sheet'
    inner_sheet = st.selectbox('Choose the inner sheet:', sheet_names)

    # Read the sheets into dataframes
    df1 = pd.read_excel(excel_file, sheet_name=sheet_names[0])
    df2 = pd.read_excel(excel_file, sheet_name=sheet_names[1])

    # Assign dfinner and dfouter based on user selection
    if inner_sheet == sheet_names[0]:
        dfinner = df1
        dfouter = df2
    else:
        dfinner = df2
        dfouter = df1

    # Display dataframes in the app
    st.write('Inner sheet (dfinner):', inner_sheet)
    st.write(dfinner.head())
    st.write('Outer sheet (dfouter):', sheet_names[1] if inner_sheet == sheet_names[0] else sheet_names[0])
    st.write(dfouter.head())

if __name__ == '__main__':
    main()