import streamlit as st
import pandas as pd
import streamlit_lottie as st_lottie
import requests
from utils import dataframe_to_csv_download_link, dataframes_to_excel_download_link
from file_processing import read_files

st.set_page_config(page_title='Clustered dataset merger', page_icon="💙")
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('style.css')
# Supress streamlit branding
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

lottie_loading_url = "https://assets6.lottiefiles.com/packages/lf20_keazd9nb.json"

with st.sidebar:
    st.title('Need more specialised help?')
    st.sidebar.write("")
    st.markdown('##### To get specialised advice and assistance on your ODK and/or Stata projects, reach out via: ')
    st.markdown('[LinkedIn](https://www.linkedin.com/in/jweinert1997/)')
    st.markdown('[Github](https://github.com/JonasWeinert/)')
    st.markdown('[Email](emailto:jnas.weinert@gmail.com)')
    st.markdown('---')
    st.header('This project')
    st.markdown('- [Request a feature](https://github.com/JonasWeinert/ClusterDatasetMerger/issues)')
    st.markdown('- [Contribute on GitHub](https://github.com/JonasWeinert/ClusterDatasetMerger/)')
    st.markdown('---')
    st.header('Was this helpful to you? ')
    st.markdown('- [Buy me a coffee](#)')
    st.markdown('---')

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def merge():
    st.title('Dataset merger')
    st.markdown('This website merges two datasets in long format. While it was developed to merge different-level (or repeated) datasets like household data ([see here for an example](https://dhsprogram.com/data/Merging-datasets.cfm)), you can also merge any other two datasets in [long format](https://towardsdatascience.com/long-and-wide-formats-in-data-explained-e48d7c9a06cb).') # First paragraph


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
                        #with st.spinner("Processing..."):
                            #st_lottie.st_lottie(load_lottie_url(lottie_loading_url), speed=1, width=200, height=200)
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
            st.error(f"Error loading files")

if __name__ == '__main__':
    merge()
st.markdown('---')
with st.expander("Privacy and legal note"):
    st.markdown('Functional Cookies: This app uses functional cookies to enhance your user experience on our webapp. These cookies are essential for the basic functionality of the webapp, such as remembering your preferences, providing security, and improving site performance. No personal data is collected. Please note that by using this webapp, you agree to this use of functional cookies. You can, however, disable cookies through your browser settings, but this may affect the functionality of the webapp. Legal Note: This app is provided "as is" without any representations or warranties, express or implied. This app makes no representations or warranties in relation to the information, services, or materials provided on our webapp. This app does not accept liability for any inaccuracies, errors, or omissions in the information, services, or materials provided on our webapp. By using this webapp, you acknowledge that the information and services may contain inaccuracies or errors, and This app  expressly excludes liability for any such inaccuracies or errors to the fullest extent permitted by law. This app is not responsible or liable for any outcomes or consequences resulting from the use of the webapp or any of its features. You agree that your use of the webapp is at your sole risk, and you assume full responsibility for any decisions or actions taken based on the information or materials provided. By using This app, you agree to indemnify, defend, and hold harmless This app and its creator from and against any and all claims, liabilities, damages, losses, or expenses, including reasonable attorneys fees and costs, arising out of or in any way connected with your access to or use of the webapp.')
