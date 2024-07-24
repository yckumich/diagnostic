import pandas as pd
import numpy as np
import warnings
import streamlit as st

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.units import inch

from io import BytesIO
import base64
warnings.filterwarnings("ignore")


# Function to generate PDF
def generate_base64pdf(dataframe):
    pdf_file = BytesIO()
    dataframe_to_pdf(dataframe, pdf_file)
    pdf_file.seek(0)
    # Encode PDF to base64
    base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')

    return base64_pdf

def remove_stars(s: str) -> str:
    if s.endswith('**'):
        return s.replace("**","").strip()
    elif s.endswith('*'):
        return s.replace("*","").strip()
    return s.strip()
def generate_tests_summary(tests_by_tier_long: pd.DataFrame):
    """
    Generates a summary of diagnostic tests by their respective tiers from the given DataFrame.

    The function processes the input DataFrame `tests_by_tier_long` to categorize tests into primary, secondary, 
    and tertiary tiers. It then cleans the data by removing duplicates, filtering out irrelevant rows, and mapping
    test formats and desired test locations to numerical values. The function identifies tests that need specimen 
    transport and those that are placed at the desired test location. It removes redundant placements and compiles 
    the final summary in a formatted DataFrame.

    Parameters:
    - tests_by_tier_long (pd.DataFrame): A DataFrame containing columns such as 'Custom Test Tier', 'Test Name', 
      'Test Name Pretty', 'Test Format', 'Test Format Lancet Tier', 'Laboratory', and 'DesiredTestLocation'.

    Returns:
    - pd.DataFrame: A formatted DataFrame summarizing the diagnostic tests by their respective tiers (Primary, 
      Secondary, and Tertiary) and services (laboratories).
    """
    
    test_by_tier_long_desiredprimary = tests_by_tier_long[tests_by_tier_long['Custom Test Tier'] == "Primary"]
    test_by_tier_long_desiredprimary = test_by_tier_long_desiredprimary.drop(columns=['Custom Test Tier',])
    test_by_tier_long_desiredprimary = test_by_tier_long_desiredprimary.drop_duplicates()
    test_by_tier_long_desiredprimary['desired_test_location'] = "Primary"
    
    # Filtering for Primary or Secondary condition tier
    test_by_tier_long_desiredsecondary = tests_by_tier_long[
        (tests_by_tier_long['Custom Test Tier'] == "Primary") | 
        (tests_by_tier_long['Custom Test Tier'] == "Secondary")
    ]
    
    test_by_tier_long_desiredsecondary = test_by_tier_long_desiredsecondary.drop(columns=['Custom Test Tier',])
    test_by_tier_long_desiredsecondary = test_by_tier_long_desiredsecondary.drop_duplicates()
    test_by_tier_long_desiredsecondary['desired_test_location'] = "Secondary"
    
    # Filtering for Primary, Secondary, or Tertiary condition tier
    test_by_tier_long_desiredtertiary = tests_by_tier_long[
        (tests_by_tier_long['Custom Test Tier'] == "Primary") | 
        (tests_by_tier_long['Custom Test Tier'] == "Secondary") | 
        (tests_by_tier_long['Custom Test Tier'] == "Tertiary")
    ]
    
    test_by_tier_long_desiredtertiary = test_by_tier_long_desiredtertiary.drop(columns=['Custom Test Tier',])
    test_by_tier_long_desiredtertiary = test_by_tier_long_desiredtertiary.drop_duplicates()
    test_by_tier_long_desiredtertiary['desired_test_location'] = "Tertiary"
    
    # Combining all filtered dataframes
    tests_by_tier_long = pd.concat([
        test_by_tier_long_desiredprimary, 
        test_by_tier_long_desiredsecondary, 
        test_by_tier_long_desiredtertiary
    ]).reset_index(drop=True)
        
    # Filter out rows where TestNameOriginal is 'no medicine-related tests'
    tests_by_tier_long = tests_by_tier_long[tests_by_tier_long['Test Name'] != 'no medicine-related tests']
    
    # Choose which name to use
    tests_by_tier_long['Test Name'] = tests_by_tier_long['Test Name Pretty']
    
    # Remove duplicate rows if test names are the same
    tests_by_tier_long = tests_by_tier_long.drop(columns=['Test Name Short', 'Test Name Pretty'])
    tests_by_tier_long = tests_by_tier_long.drop_duplicates().reset_index(drop=True)
    
    # Initialize new columns with NaN
    tests_by_tier_long['test_format_lancet_tier_num'] = np.nan
    tests_by_tier_long.loc[tests_by_tier_long['Test Format Lancet Tier'] == 'Primary', 'test_format_lancet_tier_num'] = int(1)
    tests_by_tier_long.loc[tests_by_tier_long['Test Format Lancet Tier'] == 'Secondary', 'test_format_lancet_tier_num'] = int(2)
    tests_by_tier_long.loc[tests_by_tier_long['Test Format Lancet Tier'] == 'Tertiary', 'test_format_lancet_tier_num'] = int(3)
    
    tests_by_tier_long['desired_test_location_num'] = np.nan
    tests_by_tier_long.loc[tests_by_tier_long['desired_test_location'] == 'Primary', 'desired_test_location_num'] = int(1)
    tests_by_tier_long.loc[tests_by_tier_long['desired_test_location'] == 'Secondary', 'desired_test_location_num'] = int(2)
    tests_by_tier_long.loc[tests_by_tier_long['desired_test_location'] == 'Tertiary', 'desired_test_location_num'] = int(3)
    
    # Initialize new columns with NaN
    tests_by_tier_long['placed'] = np.nan
    tests_by_tier_long['spectransport'] = np.nan
    
    tests_by_tier_long.loc[tests_by_tier_long['test_format_lancet_tier_num'] <= tests_by_tier_long['desired_test_location_num'], 'placed'] = 'Placed'
    tests_by_tier_long.loc[tests_by_tier_long['test_format_lancet_tier_num'] > tests_by_tier_long['desired_test_location_num'], 'spectransport'] = 'SpecimenTransport'
    
    # Filter out rows where both 'placed' and 'spectransport' are NaN
    tests_by_tier_long_clean = tests_by_tier_long[tests_by_tier_long['placed'].notna() | tests_by_tier_long['spectransport'].notna()]
    
    # Separate the cleaned data into 'placed' and 'spectransport'
    tests_by_tier_long_placed = tests_by_tier_long_clean[tests_by_tier_long_clean['placed'].notna()]
    tests_by_tier_long_spectransport = tests_by_tier_long_clean[tests_by_tier_long_clean['spectransport'].notna()]
    
    tests_by_tier_long_placed = tests_by_tier_long_placed.sort_values(
        by=['Laboratory', 'Test Name', 'Test Format', 'Test Format Lancet Tier','desired_test_location'], key=lambda col: col.str.lower()
    ).reset_index(drop=True)
    
    tests_by_tier_long_spectransport = tests_by_tier_long_spectransport.sort_values(
        by=['Laboratory', 'Test Name', 'Test Format', 'Test Format Lancet Tier', 'desired_test_location'], key=lambda col: col.str.lower()
    ).reset_index(drop=True)
    
    tests_placed_tmp = tests_by_tier_long_placed['Test Name'].unique()
    
    
    # Loop over each unique TestNameOriginal
    for ptest in tests_placed_tmp:
        # Filter the DataFrame for the current TestNameOriginal
        test_df_tmp = tests_by_tier_long_placed[tests_by_tier_long_placed['Test Name'] == ptest]
        
        # Get unique Test.Format values for the current test_df_tmp
        formats_placed_tmp = test_df_tmp['Test Format'].unique()
    
    
        # Loop over each unique Test.Format
        for pformat in formats_placed_tmp:
            # Filter the DataFrame for the current Test.Format
            test_format_df_tmp = test_df_tmp[test_df_tmp['Test Format'] == pformat]
    
            # Get the minimum DesiredTestLocationNum for the current TestNameOriginal and Test.Format
            lowest_tier_placed = test_format_df_tmp['desired_test_location_num'].min()
    
            indices_remove_placement = tests_by_tier_long_placed[
                (tests_by_tier_long_placed['desired_test_location_num'] > lowest_tier_placed) &
                (tests_by_tier_long_placed['Test Name'] == ptest) &
                (tests_by_tier_long_placed['Test Format'] == pformat)
            ].index
         
            # Set 'placed' to NaN for these indices
            tests_by_tier_long_placed.loc[indices_remove_placement, 'placed'] = np.nan
            
    tests_by_tier_long_placed = tests_by_tier_long_placed.dropna(subset=['placed'])
    tests_by_tier_long_clean = pd.concat([tests_by_tier_long_placed, tests_by_tier_long_spectransport])
    
    tests_by_tier_long_clean = tests_by_tier_long_clean.sort_values(
        by=['Laboratory', 'Test Name', 'Test Format', 'Test Format Lancet Tier', 'desired_test_location'], key=lambda col: col.str.lower()
    ).reset_index(drop=True)
    
    tests_out = pd.DataFrame(columns=['Diagnostics', 'Tier'])
    
    i = 0
    seperator = ';_;'
    
    for level in tests_by_tier_long_clean['desired_test_location'].unique():
        filtered_tests_clean = tests_by_tier_long_clean[
            (tests_by_tier_long_clean['desired_test_location'] == level) & 
            (tests_by_tier_long_clean['placed'] == 'Placed')
        ]
        
        for f in filtered_tests_clean['Test Format'].unique():
            # Append a new row with NaN values using pd.concat
            new_row = pd.DataFrame({'Diagnostics': [np.nan], 'Tier': [level]})
            tests_out = pd.concat([tests_out, new_row], ignore_index=True)
            
            tests_in_format_tmp = filtered_tests_clean[
                (filtered_tests_clean['Test Format'] == f) & 
                (filtered_tests_clean['desired_test_location'] == level) & 
                (filtered_tests_clean['placed'] == 'Placed')
            ]['Test Name']
            
            t_str = f + ': '
            
            for t in tests_in_format_tmp:
                spectrans_to = tests_by_tier_long_spectransport[
                    (tests_by_tier_long_spectransport['Test Name'] == t) & 
                    (tests_by_tier_long_spectransport['Test Format'] == f) & 
                    (tests_by_tier_long_spectransport['Test Format Lancet Tier'] == level)
                ]['Test Format Lancet Tier']
                
                spectrans_from = tests_by_tier_long_spectransport[
                    (tests_by_tier_long_spectransport['Test Name'] == t) & 
                    (tests_by_tier_long_spectransport['Test Format'] == f)
                ]['desired_test_location']
                
                if len(spectrans_to) == 1:
                    t_str += t + f'*{seperator}'
                elif len(spectrans_to) == 2:
                    t_str += t + f'**{seperator}'
                elif len(spectrans_to) == 0:
                    t_str += t + f'{seperator}'
            
            # Remove the trailing '; '
            t_str = t_str.rstrip(seperator)
            tests_out.at[i, 'Diagnostics'] = t_str
            i += 1
    
    # Remove rows where 'Diagnostics' is NaN
    tests_out = tests_out.dropna(subset=['Diagnostics'])

    #------ YCK POST PROCESSING -------
    tests_out_seperated = list()
    
    for _,row in tests_out.iterrows():
        temp_diagonostic = row['Diagnostics']
        temp_test_format = temp_diagonostic.split(":")[0]
        temp_tests = temp_diagonostic.split(":")[1].split(seperator)
        temp_tier = row['Tier']
        for test in temp_tests:
            temp_lab = tests_by_tier_long_clean[
                                (tests_by_tier_long_clean['Test Name']==remove_stars(test)) &
                                (tests_by_tier_long_clean['Test Format']==temp_test_format)
            ]['Laboratory'].unique()
            temp_lab = ", ".join(temp_lab)
            tests_out_seperated.append({"service": temp_lab,"test_format":temp_test_format, "test_name":test, "tier": temp_tier})
    
    tests_out_seperated_df = pd.DataFrame.from_dict(tests_out_seperated)
    
    formatted_out_list = list()
    
    for service, service_df in tests_out_seperated_df.groupby(by='service'):
        max_row_num = max(service_df['tier'].value_counts())
        tmp_pri_df = service_df[service_df['tier']=='Primary'].sort_values(by=['test_format', 'test_name']).reset_index(drop=True)
        tmp_sec_df = service_df[service_df['tier']=='Secondary'].sort_values(by=['test_format', 'test_name']).reset_index(drop=True)
        tmp_ter_df = service_df[service_df['tier']=='Tertiary'].sort_values(by=['test_format', 'test_name']).reset_index(drop=True)
    
        for i in range(max_row_num):
            tmp_pri_val = "-" if tmp_pri_df.shape[0] <= i else str(tmp_pri_df.loc[i]["test_format"] + ": " + tmp_pri_df.loc[i]['test_name'])
            tmp_sec_val = "-" if tmp_sec_df.shape[0] <= i else str(tmp_sec_df.loc[i]["test_format"] + ": " + tmp_sec_df.loc[i]['test_name'])
            tmp_ter_val = "-" if tmp_ter_df.shape[0] <= i else str(tmp_ter_df.loc[i]["test_format"] + ": " + tmp_ter_df.loc[i]['test_name'])
            formatted_out_list.append({
                'service': service,
                'primary': tmp_pri_val,
                'secondary': tmp_sec_val, 
                'tertiary': tmp_ter_val,
            })
            
    return pd.DataFrame.from_dict(formatted_out_list)

def display_test_by_lab_df(df_list):

    df = pd.DataFrame.from_dict(df_list)
    column_config = {col: st.column_config.Column(disabled=True,) for col in df.columns if col != 'Custom Test Tier'}
    column_config['Custom Test Tier'] = st.column_config.SelectboxColumn(
            help='Custom Condition Tier',
            options=['Primary','Secondary','Tertiary'],
            required=True,
    )
    df["delete"] = False

    # Make Delete be the first column
    df = df[["delete"] + df.columns[:-1].tolist()]

    st.data_editor(
        df,
        key="test_summary_editor",
        on_change=test_summary_delete_callback,
        hide_index=False,
        column_config=column_config,
        use_container_width=True,
        height=1000,
    )

def test_summary_delete_callback():
    """
    Callback function to delete rows from the custom condition list based on user interaction.
    If the 'delete' checkbox is checked for a row, that row is removed from the custom condition list.
    """

    edited_rows = st.session_state["test_summary_editor"]["edited_rows"]
    for idx, value in edited_rows.items():
        if ('delete' in value.keys()) and (value["delete"] is True):
            st.session_state["curr_clstbls_list"].pop(idx)
        else:
            for k,v in value.items():
                st.session_state["curr_clstbls_list"][idx][k] = v
    
    st.session_state.test_summary_df = generate_tests_summary(pd.DataFrame.from_dict(st.session_state.curr_clstbls_list))
            


def wrap_text(text, style):
    return Paragraph(text, style)

def get_merge_span(item_list):
    merge_indices = []
    curr_val, start_idx, end_idx = item_list[0], 1, 1

    for val in item_list[1:]:
        if val == curr_val:
            end_idx += 1
        else:
            curr_val = val
            merge_indices.append([start_idx, end_idx])
            start_idx = end_idx + 1
            end_idx += 1

    merge_indices.append([start_idx, end_idx])
    return merge_indices

def dataframe_to_pdf(dataframe, pdf_file='output.pdf'):
    pdf = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        topMargin=0.35 * inch,
        bottomMargin=0.35 * inch
    )    
    
    elements = []

    # Define the styles
    style = getSampleStyleSheet()
    header_style = ParagraphStyle(
        name='HeaderStyle',
        parent=style['BodyText'],
        fontName='Helvetica-Bold',
        fontSize=10,
        alignment=1,  # Center alignment
        leading=14,   # Line height
        spaceBefore=6,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        name='BodyStyle',
        parent=style['BodyText'],
        fontSize=8,
        alignment=1,  # Center alignment
        leading=10,   # Line height
        spaceBefore=6,
        spaceAfter=6
    )

    # Define the style for the table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), Color(211/255, 211/255, 211/255)),  # Grey background for header
        ('TEXTCOLOR', (0, 0), (-1, 0), Color(255/255, 255/255, 255/255)),   # White text for header
        ('BACKGROUND', (0, 1), (0, -1), Color(240/255, 240/255, 240/255)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (1, 1), (-1, -1), Color(255/255, 255/255, 255/255)), # White background for body
        ('GRID', (0, 0), (-1, -1), 1, Color(55/255, 55/255, 55/255)),       # Black grid lines
        ('VALIGN', (1, 1), (-1, -1), 'MIDDLE'),  # Vertically align text in the first column to the middle
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE')    # Vertically align text in the first column to the middle
    ])

    # Define column widths
    col_widths = [1 * inch, 2.15 * inch, 2.15 * inch, 2.15 * inch]

    # Split the DataFrame into chunks
    max_rows_per_page = 22  # Adjust based on your page size and content
    chunks = [dataframe.iloc[i:i + max_rows_per_page] for i in range(0, dataframe.shape[0], max_rows_per_page)]

    for chunk in chunks:
        # Prepare data for the table, wrapping text to fit the column width
        data = []

        # Wrap column headers separately to apply the header style
        wrapped_headers = [wrap_text(col, header_style) for col in dataframe.columns]
        data.append(wrapped_headers)

        # Wrap body cells with the body style
        for index, row in chunk.iterrows():
            wrapped_row = [wrap_text(str(row[col]), body_style) for col in dataframe.columns]
            data.append(wrapped_row)

        # Create the table
        table = Table(data, colWidths=col_widths)

        # Apply the merging spans to the table
        merge_indices = get_merge_span(chunk['service'].tolist())
        for start, end in merge_indices:
            table_style.add('SPAN', (0, start), (0, end))
            table_style.add('VALIGN', (0, start), (0, end), 'MIDDLE')  # Ensure vertical alignment in merged cells

        table.setStyle(table_style)
        elements.append(table)
        elements.append(PageBreak())

    # Build the PDF
    pdf.build(elements)


def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def add_sidebar():
    with st.sidebar:
        st.markdown("""
        # Diagnostic Test Summary Instructions

        Welcome to the **Diagnostic Test Summary** page. This page is designed to help you generate a comprehensive summary of diagnostic tests categorized by their respective tiers. Follow the instructions below to make the most out of this functionality.

        ## Purpose
        The **Diagnostic Test Summary** page allows you to:
        1. **Fetch the existing Lab Specific - Test By Laboratory table**.
        2. **Generate and view a summary of diagnostic tests** categorized into primary, secondary, and tertiary tiers.
        3. **Manage the custom test tiers and their respective diagnostic tests**.

        ## Steps to Use This Page

        ### Step 1: Create/Upload Custom Test Tier
        Before generating the test summary, ensure you have created or uploaded a custom test tier. This can be done on the **Build Custom Test Tier** page. If you have already done this, you will see the "Custom Test Tier" column displayed in the "Test By Laboratory" table on the Diagnostic Test Dashboard under the Lab Specific tab

        ### Step 2: Fetch the Current "Test By Laboratory" Table
        If the "Lab Specific - Test By Laboratory" table is not displayed, click on the "Fetch current 'Test By Laboratory' table" button. This will load the table based on your custom test tier.

        ### Step 3: Manage Current Table
        Once the table is fetched and displayed, you have the following options:
        - **Refresh Current Table**: Click this button to fetch the latest table.
        - **Delete Current Table**: Click this button to delete the current table.
        - **Generate Test Summary**: Click this button to generate the test summary based on the current table.

        ### Step 4: View Test Summary
        After generating the test summary, it will be displayed in the "Test Summary" section. You can view the summary of diagnostic tests categorized into primary, secondary, and tertiary tiers.

        ### Step 5: Edit Test Summary
        You can edit the test summary using the data editor. To delete a row, check the "delete" checkbox next to the row. The row will be removed from the custom condition list. (After the edit, you must click **Generate Test Summary** to reflect the changed to summary table)

        ## Notes
        - The **Generate Test Summary** button will process the custom test tiers and generate a comprehensive summary of diagnostic tests.
        - Ensure that you have created or uploaded the custom test tier and check the generated Lab Specific - Test By Laboratory table before attempting to generate the test summary.
        - Use the "Refresh Current Table" and "Delete Current Table" buttons to manage the current table effectively.
        """)

    

# def summary_get_lab_specific_test_by_laboratory_section(df):
#     print("before df.shape: ", df.shape)
#     columns = [
#         'laboratory',
#         'testname',
#         'test_name_short',
#         'test_name_pretty',
#         'test_format',
#         'test_format_lancet_tier',
#         'custom_test_tier',
#     ]
#     rename_map = {
#         'laboratory': 'Laboratory',
#         'testname': 'Test Name',
#         'test_name_short': 'Test Name Short',
#         'test_name_pretty': 'Test Name Pretty',
#         'test_format': 'Test Format',
#         'test_format_lancet_tier': 'Test Format Lancet Tier',
#         'custom_test_tier': 'Custom Test Tier',
#     }
#     df = df[columns].copy()

#     df.rename(
#             columns=rename_map,
#             inplace=True,
#             )
#     df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
#     print("after df.shape: ", df.shape)
#     return df 


# empty_selection = {
#     'Diagnostic': {
#         'Laboratory': ['Blood bank'], 
#         'Test Format': [], 
#         'Test Reason': [], 
#         'Category': []
#     }, 
#     'Medicine': {
#         'Medicine': []
#     }, 
#     'Condition': {
#         'High Burden Disease': [], 
#         'Clinical Service': [], 
#         'Condition Name': []
#     }, 
#     'WHO EDL/EML': {
#         'WHO EDL v2': [],
#         'WHO EDL v2 Tier': [],
#         'WHO EML v20': [], 
#         'EML Category': []
#     }
# }