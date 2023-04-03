
# Data Merger

Check it out [here](https://dataset-merge.streamlit.app/).

Streamlit Data Merger is a web application that allows users to merge two datasets using a common unique identifier. The app supports uploading Excel and CSV files and provides the merged dataset as a downloadable CSV or Excel file with three sheets: outer, inner, and merged data.

## Features

-   Upload multiple Excel (`.xlsx`) or CSV (`.csv`) files.
-   Select the inner and outer datasets from the uploaded files.
-   Choose the unique identifier columns for both datasets from a dropdown list.
-   Check whether the unique identifier columns have the same data type.
-   Display the number of matches made based on the unique identifier.
-   Download the merged dataset as a CSV or Excel file.

## Installation

1.  Clone this repository or download the source code.
    
2.  Navigate to the project directory and create a virtual environment:
    
    bashCopy code
    
    `python -m venv venv` 
    
3.  Activate the virtual environment:
    
    -   For Windows:
        
        bashCopy code
        
        `venv\Scripts\activate` 
        
    -   For macOS and Linux:
        
        bashCopy code
        
        `source venv/bin/activate` 
        
4.  Install the required packages:
    
    bashCopy code
    
    `pip install -r requirements.txt` 
    
5.  Run the Streamlit app:
    
    bashCopy code
    
    `streamlit run app.py` 
    
6.  Open the displayed URL in your web browser to access the app.
    

## Usage

1.  Upload Excel or CSV files containing the datasets you want to merge.
2.  Select the inner and outer datasets from the uploaded files.
3.  Choose the unique identifier columns for both datasets.
4.  View the merged dataset and the number of matches made based on the unique identifier.
5.  Download the merged dataset as a CSV or Excel file.

## Dependencies

-   streamlit
-   pandas
-   openpyxl
-   xlsxwriter
-   streamlit-lottie
-   requests

----------
