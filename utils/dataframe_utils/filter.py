"""
This dictionary maps high-level filters to their corresponding low-level filters. 
The format of the dictionary is:
High-level filter: {Lower-level filter title: Lower-level filter column name}.
"""

high_level_filter_map = {
    'Diagnostic': {
        'Laboratory': 'laboratory',
        'Test Format': 'test_format',
        'Test Reason': 'testreason',
        'Category': 'category'
    },
    'Medicine': {
        'Medicine': 'medicine'
    },
    'Condition': {
        'High Burden Disease': 'higherpriority',
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
        "Lancet GBD": 'lancet_gbd',
        "Lancet Health Tier": 'lancet_condition_tier',
        "Test Format Lancet Tier" :'test_format_lancet_tier', 
        "Lancet Test Tier Capacity" :'lancet_test_tier_capacity' , 
        "Test Name" :'testname',
        "Test Format Lancet Include" :'test_format_lancet_include',
        "Lancet Indication Exclude" :'lancet_indication_exclude',
    }
}