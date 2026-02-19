"""
This dictionary maps high-level filters to their corresponding low-level filters. 
The format of the dictionary is:
High-level filter: {Lower-level filter title: Lower-level filter column name}.
"""

high_level_filter_map = {
    'Diagnostic': {
        'Diagnostic': 'test_name_pretty',        
        'Domain': 'laboratory',
        'Diagnostic Format': 'test_format',
        'Diagnostic Reason': 'testreason',
        'Diagnostic Reason Category': 'category'
    },
    'Medicine': {
        'Medicine': 'medicine'
    },
    'Condition': {
        'Clinical Service': 'clinical_service',
        'Condition Name':'conditionname'
    },
    'WHO EDL/EML': {
        'WHO EDL v2':'who_edl_v2',
        'WHO EDL v2 Tier': 'who_edl_v2_tier',
        'WHO EML v20': 'who_eml_v20',
        'EML Category': 'eml_cat_1'
    },
    "Lancet": {
        "Lancet High Burden Disease": 'lancet_gbd',
        "Lancet Condition Tier": 'lancet_condition_tier',
        "Test Format Lancet Tier" :'test_format_lancet_tier', 
        "Test Name" :'testname',
        "Test Format Lancet Include" :'test_format_lancet_include',
        "Lancet Indication Exclude" :'lancet_indication_exclude',
    }
}