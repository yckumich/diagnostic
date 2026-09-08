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

name_map = {"test_format": "Diagnostic Format", "custom_test_tier": "Diagnostic Format Custom Tier"}
DATA_FRAME_HEIGHT = 800

def _reset_test_summary() -> None:
    """Hide both summary tabs and clear cached dataframe."""
    st.session_state.display_test_summary = False
    st.session_state.test_summary_df = None


def display_placeholder_message(long_format_tab, pdf_tab):
    message = generate_placeholder_message()
    for tab in [long_format_tab, pdf_tab]:
        with tab:
            st.markdown(f"""<div style="height:400px;"></div>{message}""", unsafe_allow_html=True)


def generate_placeholder_message():
    if not st.session_state.custom_condition_list and not st.session_state.custom_test_tier_list:
        return "<h2 style='text-align:center;color:grey'>Upload both tier tables first</h2>"
    if not st.session_state.custom_condition_list:
        return "<h2 style='text-align:center;color:grey'>Upload the condition-tier table on Page 2 first</h2>"
    if not st.session_state.custom_test_tier_list:
        return "<h2 style='text-align:center;color:grey'>Upload the test-format-tier table on Page 3 first</h2>"
    return "<h2 style='text-align:center;color:grey'>Press <b>Generate Diagnostic Summary</b> on the left to continue</h2>"


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

# utils/tests_summary_utils/utils.py
def generate_and_display_test_summary(input_key: str):

    label = "Generate Diagnostic Summary"
    btn_key = f"gen_summary_btn_{input_key}" 

    if st.button(label, key=btn_key):        
        tests_long = generate_tests_by_tier_long()

        if tests_long is None:
            _reset_test_summary()
            st.toast("Need both diagnostic format and condition tier tables", icon="⚠️")
            st.rerun()

        result = generate_tests_summary(tests_long)
        if result.empty:
            _reset_test_summary()
            st.toast("No matching tests found — check that your condition and test-format tier selections overlap with the data.", icon="⚠️")
            st.rerun()

        st.session_state.test_summary_df = result
        st.session_state.display_test_summary = True
        st.rerun()


def generate_tests_by_tier_long():
    if not st.session_state.custom_condition_list or not st.session_state.custom_test_tier_list:
        return None

    from data.database import get_view_df
    cached_clstbls_df_all_cols = get_view_df()
    
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
    
    if not tests_out_seperated:
        return pd.DataFrame(columns=['service', 'tier', 'test_format', 'test_name'])

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


def get_merge_span(item_list: list[str]) -> list[tuple[int, int]]:
    """
    Returns a list of (start_row, end_row) pairs **1-based** (row 0 is header).

    Works even when `item_list` is empty or has a single entry.
    """
    if not item_list:          # completely empty chunk – nothing to span
        return []

    merge_indices = []
    curr_val = item_list[0]
    start_idx = end_idx = 1    # row-0 is header → body starts at 1

    for val in item_list[1:]:
        if val == curr_val:
            end_idx += 1
        else:
            merge_indices.append((start_idx, end_idx))
            curr_val = val
            start_idx = end_idx = end_idx + 1

    # close the last run
    merge_indices.append((start_idx, end_idx))
    return merge_indices


def dataframe_to_pdf(dataframe, pdf_file: str | BytesIO = "output.pdf"):
    """
    Render `dataframe` to a paginated PDF, one table per page.

    **NEW:** spans on the *service* column are clipped so they can
    never run past the bottom of the current page chunk.
    """
    pdf = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        topMargin=0.35 * inch,
        bottomMargin=0.35 * inch,
    )
    elements = []

    # --- styles ---------------------------------------------------
    style = getSampleStyleSheet()
    header_style = ParagraphStyle(
        "HeaderStyle",
        parent=style["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=10,
        alignment=1,
        leading=14,
        spaceBefore=6,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=style["BodyText"],
        fontSize=8,
        alignment=1,
        leading=10,
        spaceBefore=6,
        spaceAfter=6,
    )

    base_table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), Color(211 / 255, 211 / 255, 211 / 255)),
            ("TEXTCOLOR", (0, 0), (-1, 0), Color(1, 1, 1)),
            ("BACKGROUND", (0, 1), (0, -1), Color(240 / 255, 240 / 255, 240 / 255)),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (1, 1), (-1, -1), Color(1, 1, 1)),
            ("GRID", (0, 0), (-1, -1), 1, Color(55 / 255, 55 / 255, 55 / 255)),
            ("VALIGN", (1, 1), (-1, -1), "MIDDLE"),
            ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
        ]
    )

    col_widths = [1 * inch, 2.15 * inch, 2.15 * inch, 2.15 * inch]
    max_rows_per_page = 16

    for chunk in (
        dataframe.iloc[i : i + max_rows_per_page]
        for i in range(0, len(dataframe), max_rows_per_page)
    ):
        data = [[wrap_text(col, header_style) for col in dataframe.columns]]
        for _, row in chunk.iterrows():
            data.append([wrap_text(str(row[c]), body_style) for c in dataframe.columns])

        table = Table(data, colWidths=col_widths)
        tbl_style = TableStyle(base_table_style.getCommands())  # copy

        # ---- safe spanning --------------------------------------
        merge_indices = get_merge_span(chunk["service"].tolist())
        last_body_row = len(chunk)          # 1-based index of last body row
        for start, end in merge_indices:
            if start > last_body_row:           # all rows are on previous page
                continue
            end = min(end, last_body_row)       # clamp to page bottom
            if end > start:                     # only span if >1 row
                tbl_style.add("SPAN", (0, start), (0, end))
                tbl_style.add("VALIGN", (0, start), (0, end), "MIDDLE")

        table.setStyle(tbl_style)
        elements.append(table)
        elements.append(PageBreak())

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
            "Download Diagnostic Summary",
            convert_df(st.session_state.test_summary_df),
            "test_summary.csv",
            "text/csv",
            key='download-csv'
        )

# ------------------------------------------------------------------
# 1.  CALLBACKS – operate directly on the master lists
# ------------------------------------------------------------------
def _delete_rows_from_list(edited_rows: dict, target_list: list) -> None:
    """Shared logic for both condition & test-format grids."""
    to_del = sorted([i for i, v in edited_rows.items() if v.get("delete")], reverse=True)
    for i in to_del:
        if i < len(target_list):
            target_list.pop(i)

    for i, v in edited_rows.items():
        if i in to_del:
            continue
        for k, val in v.items():
            if k != "delete":
                target_list[i][k] = val

    # <<< NEW: if user wiped the entire table, hide summaries >>>
    if not target_list:
        _reset_test_summary()


# CONDITION tier ---------------------------------------------------
def condition_delete_callback():
    edited = st.session_state["condition_editor"]["edited_rows"]
    _delete_rows_from_list(edited, st.session_state.custom_condition_list)
    st.session_state["_need_rerun"] = True


def condition_editor():
    df = pd.DataFrame(st.session_state.custom_condition_list).reset_index(drop=True)

    df["delete"] = False
    df = df[["delete"] + df.columns[:-1].tolist()]

    cfg = {
        "conditionname": st.column_config.Column(disabled=True, help="Condition Name"),
        "conditionlevel": st.column_config.SelectboxColumn(
            options=["triage", "moderate", "severe"], required=True
        ),
        "custom_condition_tier": st.column_config.SelectboxColumn(
            options=["Primary", "Secondary", "Tertiary"], required=True
        ),
    }

    st.data_editor(
        df,
        key="condition_editor",
        column_config=cfg,
        on_change=condition_delete_callback,
        hide_index=False,
        use_container_width=True,
        height=DATA_FRAME_HEIGHT,
    )


# TEST-FORMAT tier -------------------------------------------------
def test_tier_delete_callback():
    edited = st.session_state["test_tier_editor"]["edited_rows"]
    _delete_rows_from_list(edited, st.session_state.custom_test_tier_list)
    st.session_state["_need_rerun"] = True


def test_tier_editor():
    df = pd.DataFrame(st.session_state.custom_test_tier_list).reset_index(drop=True)
    df["delete"] = False
    df = df[["delete"] + df.columns[:-1].tolist()]

    cfg = {
        "test_format": st.column_config.Column(disabled=True),
        "custom_test_tier": st.column_config.SelectboxColumn(
            options=["Primary", "Secondary", "Tertiary"], required=True
        ),
    }

    st.data_editor(
        df,
        key="test_tier_editor",
        column_config=cfg,
        on_change=test_tier_delete_callback,
        hide_index=False,
        use_container_width=True,
        height=DATA_FRAME_HEIGHT,
    )

def inline_custom_condition_delete_callback():
    """
    Delete rows directly from the **master** list
    (`custom_condition_list`) and re-run the app so the checkbox
    clears immediately.
    """
    edited = st.session_state["inline_custom_condition_data_editor"]["edited_rows"]

    # gather indices to delete
    to_del = [i for i, v in edited.items() if v.get("delete", False)]

    # delete highest → lowest
    for i in sorted(to_del, reverse=True):
        if i < len(st.session_state.custom_condition_list):
            st.session_state.custom_condition_list.pop(i)      # <<< NEW >>>

    # apply in-row edits for rows we kept
    for i, v in edited.items():
        if i in to_del:
            continue
        for k, val in v.items():
            if k != "delete":
                st.session_state.custom_condition_list[i][k] = val   # <<< NEW >>>

    st.rerun()  # <<< NEW – forces instant refresh >>>


def inline_display_custom_condition_df():
    """
    Shows the current inline table in an editable grid.
    """
    custom_condition_df = (
        pd.DataFrame(st.session_state["inline_custom_condition_list"])
        .reset_index(drop=True)                     # <<< NEW: keep index contiguous every rerun >>>
    )

    column_config = {
        'conditionname': st.column_config.Column(disabled=True, help='Condition Name'),
        'conditionlevel': st.column_config.SelectboxColumn(
            help='Condition Level', options=['triage','moderate','severe'], required=True),
        'custom_condition_tier': st.column_config.SelectboxColumn(
            help='Condition Tier', options=['Primary','Secondary','Tertiary'], required=True)
    }
    custom_condition_df["delete"] = False
    custom_condition_df = custom_condition_df[["delete"] + custom_condition_df.columns[:-1].tolist()]

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
    if st.button("Fetch Condition Tiers Table"):
        # st.session_state.inline_custom_condition_list = st.session_state.custom_condition_list.copy()
        msg = st.toast('Fetching Condition Tiers Table...')
        time.sleep(0.7)
        msg.toast('Fetched ✅ ')
        st.rerun()


def inline_update_custom_condition_tier():
    if st.button("Update Condition Tiers Table"):
        if len(st.session_state.inline_custom_condition_list) > 0:
            st.session_state.custom_condition_list = st.session_state.inline_custom_condition_list
            msg = st.toast('Updating Condition Tiers Table...')
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
    Same safe-deletion pattern for the Test-Format tier table.
    """
    edited_rows = st.session_state["inline_test_tier_data_editor"]["edited_rows"]

    # gather indices to delete
    to_del = [idx for idx, val in edited_rows.items() if val.get("delete", False)]  # <<< NEW >>>

    # delete in reverse order
    for idx in sorted(to_del, reverse=True):                                        # <<< NEW >>>
        if idx < len(st.session_state["inline_custom_test_list"]):                  # <<< NEW >>>
            st.session_state["inline_custom_test_list"].pop(idx)

    # apply edits to surviving rows
    for idx, val in edited_rows.items():                                            # <<< NEW >>>
        if idx in to_del:
            continue
        for k, v in val.items():
            if k != "delete":
                st.session_state["inline_custom_test_list"][idx][k] = v             # <<< NEW >>>


def inline_display_custom_test_tier_df():
    """
    Editable grid for test-format tiers (with safe index reset).
    """
    custom_test_tier_df = (
        pd.DataFrame(st.session_state["inline_custom_test_list"])
        .reset_index(drop=True)                     # <<< NEW: keep index contiguous >>>
    )

    column_config = {
        'test_format': st.column_config.Column(disabled=True),
        'custom_test_tier': st.column_config.SelectboxColumn(
            options=['Primary','Secondary','Tertiary'], required=True),
    }
    custom_test_tier_df["delete"] = False
    custom_test_tier_df = custom_test_tier_df[["delete"] + custom_test_tier_df.columns[:-1].tolist()]

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
    if st.button("Fetch Diagnostic-Format Tiers Table"):
        st.session_state.inline_custom_test_list = st.session_state.custom_test_tier_list.copy()
        msg = st.toast('Fetching Diagnostic-Format Tiers Table...')
        time.sleep(0.7)
        msg.toast('Fetched ✅ ')
        st.rerun()

def inline_update_custom_test_tier():
    if st.button("Update Diagnostic-Format Tiers Table"):
        if len(st.session_state.inline_custom_test_list) > 0:
            st.session_state.custom_test_tier_list = st.session_state.inline_custom_test_list
            msg = st.toast('Updating Diagnostic-Format Tiers Table...')
            time.sleep(0.7)
            msg.toast('Updated ✅ ')
            st.rerun()
        else:
            msg = st.toast('You have not made any changes to the Diagnostic-Format Tiers table...')
            time.sleep(0.7)
            msg.toast('Refreshing page')
            st.rerun()

def add_sidebar():
    with st.sidebar:
        st.markdown("""
**Diagnostic Network Planner Results Instructions**  
Welcome to the page for visualizing results of the Diagnostic Network Planner. This page is designed to help you generate a comprehensive summary of diagnostic placement recommendations by health system tier. Follow the instructions below to make the most out of this tool.

**Purpose**

The **Diagnostic Network Planner** allows you to:
1. **Generate and view a summary of diagnostic placement recommendations** categorized into primary, secondary, and tertiary tiers.
2. **Edit the Condition Tiers and Diagnostic-Format Tiers tables and see the impact on placement recommendations.**

**Steps to Use This Page**
- **Step 1: Create/Upload a Condition Tiers table**  
Before generating the Diagnostic Summary, ensure you have set and applied a Condition-Tiers table. This can be done on the Set Condition Tiers page.
- **Step 2: Create/Upload a Diagnostic-Format Tiers table**  
Similarly, ensure you have set and applied a Diagnostic-Format Tiers table on the Set Diagnostic-Format Tiers page.
- **Step 3: View Diagnostic Network Planner Summaries and Manage Current Tables**  
Once the tables are displayed (see tabs above the left panel table), you have the following options:
    - **Generate Diagnostic Summary:** Click this button to generate the placement summary based on the current tables.
    - **Edit the Condition Tiers and Diagnostic-Format Tiers tables:** individual cells can be changed from this page and it will update the tables on the Set Condition Tiers and Set Diagnostic-Format Tiers pages. Then new Diagnostic Summaries can be generated to see the impact of changes.

**Notes**
- The **Generate Diagnostic Summary** button will process the Condition Tiers and Diagnostic-Format Tiers tables to generate a comprehensive summary of diagnostic placement recommendations.
- Ensure that you have created or uploaded the Condition Tiers and Diagnostic-Format Tiers tables as well as applied those tables from the respective pages.
- While filtering based on the Condition Tiers and Diagnostic-Format Tiers tables will affect the Essential Diagnostics Explorer, additional filters applied with the Essential Diagnostics Explorer will not affect the Condition and Diagnostic-Format Tiers tables or the Diagnostic Network Planner results.
- After generating the Diagnostic Summary with this tool, you can go back to the Essential Diagnostics Explorer to view and download all of the associations as provided in the various tables. Be sure to clear any additional filters that may be applied within the Essential Diagnostics Explorer, unless they are desired. Those filters only affect display within the Explorer.
- Importantly, only a subset of conditions have the internal associations encoded in this database to support the Diagnostic Network Planner. If you would like additional conditions encoded for the Diagnostic Network Planner, please contact us (see About).
        """)
