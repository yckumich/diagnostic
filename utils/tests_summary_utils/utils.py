import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

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
                    t_str += t + '*;'
                elif len(spectrans_to) == 2:
                    t_str += t + '**;'
                elif len(spectrans_to) == 0:
                    t_str += t + ';'
            
            # Remove the trailing '; '
            t_str = t_str.rstrip(';')
            tests_out.at[i, 'Diagnostics'] = t_str
            i += 1
    
    # Remove rows where 'Diagnostics' is NaN
    tests_out = tests_out.dropna(subset=['Diagnostics'])

    #------ YCK POST PROCESSING -------
    tests_out_seperated = list()
    
    for _,row in tests_out.iterrows():
        temp_diagonostic = row['Diagnostics']
        temp_test_format = temp_diagonostic.split(":")[0]
        temp_tests = temp_diagonostic.split(":")[1].split(";")
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



def add_sidebar():
    return "..."