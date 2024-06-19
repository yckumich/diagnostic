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
    }
}