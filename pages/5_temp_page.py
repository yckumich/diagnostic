# import pandas as pd
# from utils.tests_summary_utils.utils import *
# from utils.dataframe_utils.utils import convert_selection_to_df
# from utils.dataframe_utils.utils_center_tab import get_lab_specific_test_by_laboratory_section
# import streamlit as st
# import time
# from typing import List
# import base64


# from io import BytesIO

# # Function to generate PDF
# def generate_base64pdf(dataframe):
#     pdf_file = BytesIO()
#     dataframe_to_pdf(dataframe, pdf_file)
#     pdf_file.seek(0)
#     # Encode PDF to base64
#     base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')

#     return base64_pdf

# dataframe = pd.read_csv('jupyter_code/r_code_translate_output.csv')

# # generate base64 PDF
# base64_pdf = generate_base64pdf(dataframe)

# # Display PDF in Streamlit
# pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
# st.markdown(pdf_display, unsafe_allow_html=True)
