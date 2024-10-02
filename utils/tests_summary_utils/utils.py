import pandas as pd
import numpy as np
import warnings
import streamlit as st

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.units import inch
import time
from io import BytesIO
import base64
warnings.filterwarnings("ignore")

name_map = {"test_format": "Test Format", "custom_test_tier": "Test Format Custom Tier"}
DATA_FRAME_HEIGHT = 800


def display_placeholder_message(selected_display_option):
    message = generate_placeholder_message()
    st.markdown(f"""<div style="height:400px;"></div>{message}""", unsafe_allow_html=True)

def generate_placeholder_message():
    if (('cached_tbls_all_cols' not in st.session_state) or 
        (not isinstance(st.session_state.cached_tbls_all_cols, pd.DataFrame))):
        return "<h2 style='text-align: center; color: grey;'>Please click [Save Table] button under 'Test By Laboratory Section' table under Lab Specific tab on Diagnostic Test Dashboard page</h2>"
    elif not st.session_state.custom_condition_list and not st.session_state.custom_test_tier_list:
        return "<h2 style='text-align: center; color: grey;'>Please upload your custom condition tier and custom test format tier and click generate the summary table.</h2>"
    elif not st.session_state.custom_condition_list:
        return "<h2 style='text-align: center; color: grey;'>Please upload your custom condition tier and click generate the summary table.</h2>"
    elif not st.session_state.custom_test_tier_list:
        return "<h2 style='text-align: center; color: grey;'>Please upload your custom test format tier and click generate the summary table.</h2>"
    else:
        return "<h2 style='text-align: center; color: grey;'>Please click the 'Generate the Summary' button to display your test summary table.</h2>"


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


def generate_and_display_test_summary(input_key):
    key = "Generate Test Summary Table" if input_key == 'cond_tab' else "Generate Test  Summary Table"
    if st.button(key):
        tests_by_tier_long = generate_tests_by_tier_long()
        if not isinstance(tests_by_tier_long, pd.DataFrame):
            msg = st.toast('Must create/upload custom test format/condition tier and sav Lab Specific - Test By Laboratory table in the main Dashboard.')
            time.sleep(0.7)
            msg.toast('Refreshing Page...')
            st.rerun()
        else:
            st.session_state.test_summary_df = generate_tests_summary(tests_by_tier_long) #currently long-format
            st.session_state.display_test_summary = True
            st.rerun()


def generate_tests_by_tier_long():
    if (('cached_tbls_all_cols' not in st.session_state) or 
        (not isinstance(st.session_state.cached_tbls_all_cols, pd.DataFrame))):
        return None
    
    cached_clstbls_df_all_cols = st.session_state.cached_tbls_all_cols.drop(columns=['custom_condition_tier','custom_test_tier'])
    
    custom_condition_df = pd.DataFrame.from_dict(st.session_state.custom_condition_list)
    custom_test_df = pd.DataFrame.from_dict(st.session_state.custom_test_tier_list)

    merged_df = pd.merge(
        left=cached_clstbls_df_all_cols,
        right=custom_condition_df[['conditionname', 'conditionlevel', 'custom_condition_tier']], 
        on=['conditionname', 'conditionlevel'],
        how='left',
    )

    merged_df = pd.merge(
        left=merged_df,
        right=custom_test_df[['test_format', 'custom_test_tier']], 
        on=['test_format'],
        how='left',
    )

    columns = [ 'laboratory',
                'testname',
                'test_name_short',
                'test_name_pretty',
                'test_format',
                #'test_format_lancet_tier', #technically there is no need for this column
                #'lancet_condition_tier', #technically there is no need for this column
                'custom_condition_tier',
                'custom_test_tier',]
    
    rename_map = {
                'laboratory': 'Laboratory',
                'testname': 'Test Name',
                'test_name_short': 'Test Name Short',
                'test_name_pretty': 'Test Name Pretty',
                'test_format': 'Test Format',
                #'test_format_lancet_tier': 'Test Format Lancet Tier',
                #'lancet_condition_tier': 'Lancet Condition Tier',
                'custom_condition_tier': 'Custom Condition Tier',
                'custom_test_tier': 'Test Format Custom Tier'
                }
    merged_df = merged_df[columns].rename(columns=rename_map).dropna(axis=0).drop_duplicates()
    
    return merged_df


def generate_tests_summary(tests_by_tier_long: pd.DataFrame):
    """
    RETURNS LONG-FORMAT SUMMARY
    Generates a summary of diagnostic tests by their respective tiers from the given DataFrame.

    The function processes the input DataFrame `tests_by_tier_long` to categorize tests into primary, secondary, 
    and tertiary tiers. It then cleans the data by removing duplicates, filtering out irrelevant rows, and mapping
    test formats and desired test locations to numerical values. The function identifies tests that need specimen 
    transport and those that are placed at the desired test location. It removes redundant placements and compiles 
    the final summary in a formatted DataFrame.

    Parameters:
    - tests_by_tier_long (pd.DataFrame): A DataFrame containing columns such as 'Custom Condition Tier', 'Test Name', 
      'Test Name Pretty', 'Test Format', 'Test Format Custom Tier', 'Laboratory', and 'DesiredTestLocation'.

    Returns:
    - pd.DataFrame: A formatted DataFrame summarizing the diagnostic tests by their respective tiers (Primary, 
      Secondary, and Tertiary) and services (laboratories).
    """
    tests_by_tier_long = tests_by_tier_long[
        ['Laboratory', 'Test Name', 'Test Name Short', 'Test Name Pretty',
         'Test Format', 'Test Format Custom Tier', 'Custom Condition Tier']
    ]

    test_by_tier_long_desiredprimary = tests_by_tier_long[tests_by_tier_long['Custom Condition Tier'] == "Primary"]
    test_by_tier_long_desiredprimary = test_by_tier_long_desiredprimary.drop(columns=['Custom Condition Tier',])
    test_by_tier_long_desiredprimary = test_by_tier_long_desiredprimary.drop_duplicates()
    test_by_tier_long_desiredprimary['desired_test_location'] = "Primary"
    
    # Filtering for Primary or Secondary condition tier
    test_by_tier_long_desiredsecondary = tests_by_tier_long[
        (tests_by_tier_long['Custom Condition Tier'] == "Primary") | 
        (tests_by_tier_long['Custom Condition Tier'] == "Secondary")
    ]
    
    test_by_tier_long_desiredsecondary = test_by_tier_long_desiredsecondary.drop(columns=['Custom Condition Tier',])
    test_by_tier_long_desiredsecondary = test_by_tier_long_desiredsecondary.drop_duplicates()
    test_by_tier_long_desiredsecondary['desired_test_location'] = "Secondary"
    
    # Filtering for Primary, Secondary, or Tertiary condition tier
    test_by_tier_long_desiredtertiary = tests_by_tier_long[
        (tests_by_tier_long['Custom Condition Tier'] == "Primary") | 
        (tests_by_tier_long['Custom Condition Tier'] == "Secondary") | 
        (tests_by_tier_long['Custom Condition Tier'] == "Tertiary")
    ]
    
    test_by_tier_long_desiredtertiary = test_by_tier_long_desiredtertiary.drop(columns=['Custom Condition Tier',])
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
    tests_by_tier_long['test_format_custom_tier_num'] = np.nan
    tests_by_tier_long.loc[tests_by_tier_long['Test Format Custom Tier'] == 'Primary', 'test_format_custom_tier_num'] = int(1)
    tests_by_tier_long.loc[tests_by_tier_long['Test Format Custom Tier'] == 'Secondary', 'test_format_custom_tier_num'] = int(2)
    tests_by_tier_long.loc[tests_by_tier_long['Test Format Custom Tier'] == 'Tertiary', 'test_format_custom_tier_num'] = int(3)
    
    tests_by_tier_long['desired_test_location_num'] = np.nan
    tests_by_tier_long.loc[tests_by_tier_long['desired_test_location'] == 'Primary', 'desired_test_location_num'] = int(1)
    tests_by_tier_long.loc[tests_by_tier_long['desired_test_location'] == 'Secondary', 'desired_test_location_num'] = int(2)
    tests_by_tier_long.loc[tests_by_tier_long['desired_test_location'] == 'Tertiary', 'desired_test_location_num'] = int(3)
    
    # Initialize new columns with NaN
    tests_by_tier_long['placed'] = np.nan
    tests_by_tier_long['spectransport'] = np.nan
    
    tests_by_tier_long.loc[tests_by_tier_long['test_format_custom_tier_num'] <= tests_by_tier_long['desired_test_location_num'], 'placed'] = 'Placed'
    tests_by_tier_long.loc[tests_by_tier_long['test_format_custom_tier_num'] > tests_by_tier_long['desired_test_location_num'], 'spectransport'] = 'SpecimenTransport'
    
    # Filter out rows where both 'placed' and 'spectransport' are NaN
    tests_by_tier_long_clean = tests_by_tier_long[tests_by_tier_long['placed'].notna() | tests_by_tier_long['spectransport'].notna()]
    
    # Separate the cleaned data into 'placed' and 'spectransport'
    tests_by_tier_long_placed = tests_by_tier_long_clean[tests_by_tier_long_clean['placed'].notna()]
    tests_by_tier_long_spectransport = tests_by_tier_long_clean[tests_by_tier_long_clean['spectransport'].notna()]
    
    tests_by_tier_long_placed = tests_by_tier_long_placed.sort_values(
        by=['Laboratory', 'Test Name', 'Test Format', 'Test Format Custom Tier','desired_test_location'], key=lambda col: col.str.lower()
    ).reset_index(drop=True)
    
    tests_by_tier_long_spectransport = tests_by_tier_long_spectransport.sort_values(
        by=['Laboratory', 'Test Name', 'Test Format', 'Test Format Custom Tier', 'desired_test_location'], key=lambda col: col.str.lower()
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
        by=['Laboratory', 'Test Name', 'Test Format', 'Test Format Custom Tier', 'desired_test_location'], key=lambda col: col.str.lower()
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
                    (tests_by_tier_long_spectransport['Test Format Custom Tier'] == level)
                ]['Test Format Custom Tier']
                
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
    # return tests_out
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
    
    tests_out_seperated_df = pd.DataFrame.from_dict(tests_out_seperated)[['service','tier','test_format','test_name']].sort_values(by=['service','tier','test_format','test_name'], ascending=True).reset_index(drop=True)

    return tests_out_seperated_df

def generate_pdf_format_df(test_summary_df):
    pdf_format_list = list()
    
    for service, test_tier_format_name_df in test_summary_df.groupby(by='service'):
        for tier, test_format_name_df in test_tier_format_name_df.groupby(by='tier'):
            for test_format, test_name_df in test_format_name_df.groupby(by='test_format'):
                test_name_list = ",\t".join(list(test_name_df['test_name']))
                pdf_format_list.append({
                    'service':service,
                    'tier':tier,
                    'test_format_name_list':f"{test_format}: {test_name_list}",
                })
    
    formatted_out_list = list()
    
    for service, tier_test_format_name_list in pd.DataFrame(pdf_format_list).groupby('service'):
        max_row_num = max(tier_test_format_name_list['tier'].value_counts())
        tmp_pri_df = tier_test_format_name_list[tier_test_format_name_list['tier']=='Primary'].sort_values(by=['test_format_name_list',]).reset_index(drop=True)
        tmp_sec_df = tier_test_format_name_list[tier_test_format_name_list['tier']=='Secondary'].sort_values(by=['test_format_name_list',]).reset_index(drop=True)
        tmp_ter_df = tier_test_format_name_list[tier_test_format_name_list['tier']=='Tertiary'].sort_values(by=['test_format_name_list',]).reset_index(drop=True)
    
        for i in range(max_row_num):
            tmp_pri_val = "-" if tmp_pri_df.shape[0] <= i else str(tmp_pri_df.loc[i]['test_format_name_list'])
            tmp_sec_val = "-" if tmp_sec_df.shape[0] <= i else str(tmp_sec_df.loc[i]['test_format_name_list'])
            tmp_ter_val = "-" if tmp_ter_df.shape[0] <= i else str(tmp_ter_df.loc[i]['test_format_name_list'])
            formatted_out_list.append({
                'service': service,
                'primary': tmp_pri_val,
                'secondary': tmp_sec_val, 
                'tertiary': tmp_ter_val,
            })
    return pd.DataFrame.from_dict(formatted_out_list)


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
    max_rows_per_page = 16  # Adjust based on your page size and content
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

def display_pdf_summary():
    base64_pdf = generate_base64pdf(generate_pdf_format_df(st.session_state.test_summary_df))

    # Display PDF in Streamlit
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="{DATA_FRAME_HEIGHT}" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
    st.markdown("""<div style="height:30px;"></div>""", unsafe_allow_html=True)
    _, col, _ = st.columns([0.3, 0.4, 0.3], gap='small')
    with col:
        st.download_button(
            "Download Test Summary",
            convert_df(st.session_state.test_summary_df),
            "test_summary.csv",
            "text/csv",
            key='download-csv'
        )

## ----------------CONDITON-RELATED FUNCTIONS--------------------

def inline_custom_condition_delete_callback():
    """
    Callback function to delete rows from the custom condition list based on user interaction.
    If the 'delete' checkbox is checked for a row, that row is removed from the custom condition list.
    """

    edited_rows = st.session_state["inline_custom_condition_data_editor"]["edited_rows"]
    for idx, value in edited_rows.items():
        if ('delete' in value.keys()) and (value["delete"] is True):
            st.session_state["inline_custom_condition_list"].pop(idx)
        else:
            for k,v in value.items():
                st.session_state["inline_custom_condition_list"][idx][k] = v


def inline_display_custom_condition_df():
    """
    Displays the custom condition list as a data editor in Streamlit.
    Allows users to view and mark rows for deletion. The 'delete' column is added
    to allow users to mark rows for deletion.
    """

    custom_condition_df = pd.DataFrame(st.session_state["inline_custom_condition_list"])
    column_config = {
        'conditionname': st.column_config.Column(
            disabled=True,
            help='Condition Name'
        ),
        'conditionlevel': st.column_config.SelectboxColumn(
            help='Condition Level',
            options=['triage','moderate','severe'],
            required=True,
        ),
        'custom_condition_tier': st.column_config.SelectboxColumn(
            help='Custom Condition Tier',
            options=['Primary','Secondary','Tertiary'],
            required=True,
        )
    }
    custom_condition_df["delete"] = False

    # Make Delete be the first column
    custom_condition_df = custom_condition_df[
        ["delete"] + custom_condition_df.columns[:-1].tolist()
    ]

    st.data_editor(
        custom_condition_df,
        key="inline_custom_condition_data_editor",
        on_change=inline_custom_condition_delete_callback,
        hide_index=False,
        column_config=column_config,
        use_container_width=True,
        height=DATA_FRAME_HEIGHT,
    )


def inline_fetch_custom_condition_tier():
    if st.button("Fetch Condition Tier Table"):
        # st.session_state.inline_custom_condition_list = st.session_state.custom_condition_list.copy()
        msg = st.toast('Fetching Custom Condition Tier Table...')
        time.sleep(0.7)
        msg.toast('Fetched ✅ ')
        st.rerun()


def inline_update_custom_condition_tier():
    if st.button("Update Condition Tier Table"):
        if len(st.session_state.inline_custom_condition_list) > 0:
            st.session_state.custom_condition_list = st.session_state.inline_custom_condition_list
            msg = st.toast('Updating Custom Condition Tier Table...')
            time.sleep(0.7)
            msg.toast('Updated ✅ ')
            st.rerun()
        else:
            msg = st.toast('You have not made any changes to the custom condition tier table ')
            time.sleep(0.7)
            msg.toast('Refreshing page')
            st.rerun()


## ----------------TEST-RELATED FUNCTIONS--------------------

def inline_custom_test_delete_callback():
    """
    Callback function to delete rows from the custom test tier list based on user interaction.
    If the 'delete' checkbox is checked for a row, that row is removed from the custom test tier list.
    Otherwise, updates the values in the custom test tier list based on user edits.
    """

    edited_rows = st.session_state["inline_test_tier_data_editor"]["edited_rows"]

    for idx, value in edited_rows.items():
        if ('delete' in value.keys()) and (value["delete"] is True):
            st.session_state["inline_custom_test_list"].pop(idx)
        else:
            for k,v in value.items():
                st.session_state["inline_custom_test_list"][idx][k] = v


def inline_display_custom_test_tier_df():
    """
    Displays the custom test tier list as a data editor in Streamlit.
    Allows users to view and mark rows for deletion. The 'delete' column is added
    to allow users to mark rows for deletion.
    """

    custom_test_tier_df = pd.DataFrame(st.session_state["inline_custom_test_list"])
    column_config = {
        'test_format': st.column_config.Column(
            disabled=True,
        ),
        'custom_test_tier': st.column_config.SelectboxColumn(
            options=['Primary','Secondary','Tertiary'],
            required=True,
        )
    }
    custom_test_tier_df["delete"] = False

    # Make Delete be the first column
    custom_test_tier_df = custom_test_tier_df[
        ["delete"] + custom_test_tier_df.columns[:-1].tolist()
    ]

    st.data_editor(
        custom_test_tier_df,
        key="inline_test_tier_data_editor",
        on_change=inline_custom_test_delete_callback,
        hide_index=False,
        column_config=column_config,
        use_container_width=True,
        height=DATA_FRAME_HEIGHT,
        
    )

def inline_fetch_custom_test_tier():
    if st.button("Fetch Test Format Tier Table"):
        st.session_state.inline_custom_test_list = st.session_state.custom_test_tier_list.copy()
        msg = st.toast('Fetching Custom Test Format Tier Table...')
        time.sleep(0.7)
        msg.toast('Fetched ✅ ')
        st.rerun()

def inline_update_custom_test_tier():
    if st.button("Update Test Format Tier Table"):
        if len(st.session_state.inline_custom_test_list) > 0:
            st.session_state.custom_test_tier_list = st.session_state.inline_custom_test_list
            msg = st.toast('Updating Custom Test Format Tier Table...')
            time.sleep(0.7)
            msg.toast('Updated ✅ ')
            st.rerun()
        else:
            msg = st.toast('You have not made any changes to the custom test format tier table...')
            time.sleep(0.7)
            msg.toast('Refreshing page')
            st.rerun()

# def add_sidebar():
#     with st.sidebar:
#         st.markdown("""
#         # Diagnostic Test Summary Instructions

#         Welcome to the **Diagnostic Test Summary** page. This page is designed to help you generate a comprehensive summary of diagnostic tests categorized by their respective tiers. Follow the instructions below to make the most out of this functionality.

#         ## Purpose
#         The **Diagnostic Test Summary** page allows you to:
#         1. Generate and view a **summary of diagnostic tests** categorized into primary, secondary, and tertiary tiers.
#         2. Manage the [**Custom Condition Tiers**](/Build_Custom_Condition_Tier) and their respective diagnostic tests.
#         3. Manage the [**Custom Test-Format Tiers**](/Build_Custom_Test_Tier) and their respective diagnostic tests.

#         ## Steps to Use This Page

#         ### Step 1: Create/Upload Custom Condition Tier
#         Before generating the test summary, ensure you have created or uploaded a Custom Condition Tier. This can be done on the **Build Custom Condition Tier** page. If you have already done this, you will see the "Custom Condition Tier" column displayed in the "Test By Laboratory" table on the Diagnostic Test Dashboard under the Lab Specific tab.

#         ### Step 2: Create/Upload Custom Test-Format Tier
#         Similarly, create or upload a Custom Test-Format Tier on the [**Build Custom Test Tier**](/_Build_Custom_Test_Tier) page. This is necessary to categorize tests into different tiers.

#         ### Step 3: Manage Current Table
#         Once the table is fetched and displayed, you have the following options:
#         - **Fetch Current Table**: Click this button to fetch the latest table.
#         - **Update Current Table**: Click this button to apply the updates you created in this page to the original current table in **Build Custom Condition Tier** or **Build Custom Test Tier** page .
#         - **Generate Test Summary**: Click this button to generate the test summary based on the current tables.

#         ### Step 4: View and Edit Test Summary
#         After generating the test summary, it will be displayed in the "Test Summary" section. You can view the summary of diagnostic tests categorized into primary, secondary, and tertiary tiers.

#         ## Notes
#         - The **Generate Test Summary** button will process the Custom Condition Tiers and Custom Test-Format Tiers to generate a comprehensive summary of diagnostic tests.
#         - Ensure that you have created or uploaded the Custom Condition Tier and Custom Test-Format Tier and check the generated Lab Specific - Test By Laboratory table before attempting to generate the test summary.
#         - Use the "Fetch Current Table" and "Update Current Table" buttons to manage the current table effectively.
#         """)


def add_sidebar():
    with st.sidebar:
        st.markdown("# Display Option")
        build_options = ['Custom Condition Tier', 'Custom Test-Format Tier']
        selected_build_option = st.radio("Select Custom Table Option:", build_options, key="build_option")

        # st.markdown("### Display Options")
        display_options = ['Test Summary - Long Format', 'Test Summary - pdf']
        selected_display_option = st.radio("Select Summary Option:", display_options, key="display_option")
        st.divider()
        # Then include the instructions
        st.markdown("""
## Diagnostic Test Summary Instructions

Welcome to the **Diagnostic Test Summary** page. This page is designed to help you generate a comprehensive summary of diagnostic tests categorized by their respective tiers. Follow the instructions below to make the most out of this functionality.

## Purpose
The **Diagnostic Test Summary** page allows you to:
1. Generate and view a **summary of diagnostic tests** categorized into primary, secondary, and tertiary tiers.
2. Manage the [**Custom Condition Tiers**](/Build_Custom_Condition_Tier) and their respective diagnostic tests.
3. Manage the [**Custom Test-Format Tiers**](/Build_Custom_Test_Tier) and their respective diagnostic tests.

## Steps to Use This Page

### Step 1: Create/Upload Custom Condition Tier
Before generating the test summary, ensure you have created or uploaded a Custom Condition Tier. This can be done on the **Build Custom Condition Tier** page. If you have already done this, you will see the "Custom Condition Tier" column displayed in the "Test By Laboratory" table on the Diagnostic Test Dashboard under the Lab Specific tab.

### Step 2: Create/Upload Custom Test-Format Tier
Similarly, create or upload a Custom Test-Format Tier on the [**Build Custom Test Tier**](/_Build_Custom_Test_Tier) page. This is necessary to categorize tests into different tiers.

### Step 3: Manage Current Table
Once the table is fetched and displayed, you have the following options:
- **Fetch Current Table**: Click this button to fetch the latest table.
- **Update Current Table**: Click this button to apply the updates you created in this page to the original current table in **Build Custom Condition Tier** or **Build Custom Test Tier** page.
- **Generate Test Summary**: Click this button to generate the test summary based on the current tables.

### Step 4: View and Edit Test Summary
After generating the test summary, it will be displayed in the "Test Summary" section. You can view the summary of diagnostic tests categorized into primary, secondary, and tertiary tiers.

## Notes
- The **Generate Test Summary** button will process the Custom Condition Tiers and Custom Test-Format Tiers to generate a comprehensive summary of diagnostic tests.
- Ensure that you have created or uploaded the Custom Condition Tier and Custom Test-Format Tier and check the generated Lab Specific - Test By Laboratory table before attempting to generate the test summary.
- Use the "Fetch Current Table" and "Update Current Table" buttons to manage the current table effectively.
""")

    return selected_build_option, selected_display_option
