# Initialise project
import streamlit as st
import pandas as pd
import numpy as np

# Start Front End interface
st.set_page_config(page_title='ODK Repeat Merger', page_icon="💙")

################### Front End ###################
# Set Front End appearance
st.title('Hirarchical dataset merger') # Title
st.markdown('This website produces a dingle dataset from two datasets of different levels..') # First paragraph
st.subheader('Upload your datasets.') # Upload prompt
uploaded_file = st.file_uploader('Either multiple csv files or single xlsx file with one sheet per dataset', type='xlsx', accept_multiple_files=True) # Save file to memory for duration of session