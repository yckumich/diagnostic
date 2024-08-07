
# import pandas as pd
# from utils.condition_tier_utils.utils import *
# import streamlit as st

# # ----------------------INIT-----------------------
# st.set_page_config(
#     page_title="Custom Condition Tier",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Constants
# CONDITION_LEVELS = ["triage", "moderate", "severe", "not applicable"]
# CONDITION_TIERS = ["Primary", "Secondary", "Tertiary"]
# ESSENTIAL_COLS = ['conditionname', 'conditionlevel', 'custom_condition_tier']
# GDB_CONDITION_LIST = retrieve_gbd_conditions()

# def initialize_session_state():
#     if "custom_condition_list" not in st.session_state:
#         st.session_state.custom_condition_list = []

#     if "custom_condition_df" not in st.session_state:
#         st.session_state.custom_condition_df = None

#     if 'show_plot' not in st.session_state:
#         st.session_state['show_plot'] = False

# initialize_session_state()










# def handle_file_upload(condition_level_csv):
#     try:
#         uploaded_df = pd.read_csv(condition_level_csv)
#         uploaded_df_cols = list(uploaded_df.columns)
#         if set(uploaded_df_cols) != set(ESSENTIAL_COLS):
#             st.warning(
#                 body="columns 'conditionname', 'conditionlevel', 'custom_condition_tier' must be presented in the uploaded csv file",
#                 icon="⚠️"
#             )
#         else:
#             st.session_state["custom_condition_list"] = uploaded_df.to_dict(orient='records')
#             st.session_state['show_plot'] = False
#             st.rerun()
#     except Exception as e:
#         st.error(f"Error uploading file: {e}")

# def add_new_condition():
#     st.session_state.custom_condition_list.append(
#         {
#             "conditionname": st.session_state.conditionname,
#             "conditionlevel": st.session_state.conditionlevel,
#             "custom_condition_tier": st.session_state.custom_condition_tier,
#         }
#     )

# def render_plot():
#     fig = create_condition_plot(
#         process_condition_tiers(
#             pd.DataFrame(st.session_state["custom_condition_list"])
#         )
#     )
#     st.pyplot(fig)

#     st.markdown("""<div style="height:50px;"></div>""", unsafe_allow_html=True)
#     _, col1, col2, col3, _ = st.columns([0.23, 0.17, 0.17, 0.2, 0.23], gap='small')
#     with col1:
#         if st.button('Redraw Plot'):
#             st.rerun()
#     with col2:
#         if st.button('Delete Plot'):
#             st.session_state['show_plot'] = False
#             st.rerun()
#     with col3:
#         st.download_button(
#             label="Download Table",
#             data=pd.DataFrame(st.session_state["custom_condition_list"]).to_csv(index=False),
#             file_name='custom_condition_level.csv',
#             mime='text/csv',
#         )

# def display_add_condition_form():
#     st.write("### Add a New Custom Condition Instance ")
#     with st.form("new_condition", clear_on_submit=True):
#         st.selectbox("Condition Name", GDB_CONDITION_LIST, key="conditionname")
#         st.selectbox("Condition Level", CONDITION_LEVELS, key="conditionlevel")
#         st.selectbox("Condition Tier", CONDITION_TIERS, key="custom_condition_tier")
#         st.form_submit_button("Add", on_click=add_new_condition)

# def display_upload_csv():
#     st.write("### Upload a Custom Condition Tier CSV")
#     condition_level_csv = st.file_uploader("upload a CSV file", type={"csv", "txt"})
#     if (condition_level_csv is not None) and (st.button("Upload")):
#         handle_file_upload(condition_level_csv)
        
# def main():
#     add_sidebar()
#     build_col, display_col = st.columns([1, 1], gap="small")
    
#     with build_col:
#         st.write("### Custom Condition Tier Table")
#         display_custom_condition_df()

#         _, col_1, col_2, _ = st.columns([0.2, 0.3, 0.3, 0.2])
#         with col_1:
#             delete_current_coustom_df()
#         with col_2:
#             save_current_coustom_df()

#         display_add_condition_form()
#         display_upload_csv()

#     with display_col:
#         if len(st.session_state["custom_condition_list"]) > 1:
#             if not st.session_state['show_plot']:
#                 st.markdown("""<div style="height:500px;"></div>""", unsafe_allow_html=True)
#                 _, col, _ = st.columns([0.35, 0.3, 0.35])
#                 with col:
#                     if st.button('Render Custom Condition Tier Plot'):
#                         st.session_state['show_plot'] = True
#                         st.rerun()
#             else:
#                 render_plot()
#         else:
#             st.markdown("""<div style="height:400px;"></div>""", unsafe_allow_html=True)
#             st.markdown("<h2 style='text-align: center; color: grey;'>Must build/upload custom condition tier dataframe to render the plot</h2>", unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()
