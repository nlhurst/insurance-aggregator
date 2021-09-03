import os
import pytest

import pandas as pd

from file_combiner import FileCombiner

 
@pytest.fixture
def file_combiner():
    obj = FileCombiner()
    return obj

@pytest.fixture
def home_file():
    data = {'Provider Name': ['Home R Us', 'HomeGuard', 'WeProtect', 'HomesOnly', 'Homes4U'],
            'CampaignID': ['HOME1', 'HOME2', None, 'HOME4', 'HOME5'],
            'Cost Per Ad Click': [5, "15", 32, 3, 5], 
            'Redirect Link': ['homerus.com', 'homeguard.net', 'weprotect.com', 'homesonly.com', 'homes4u.net'],
            'Phone Number': [1234567, 1234567, 1234567, None, 1234567],
            'Address': ["123 A Street", "234 B Street", "", "", "345 C Street"], 
            'Zipcode': ["12345", "12343", "54321", "12345", "12354"],
            'Test Column': ['test', 'test', 'test', 'test', 'test']}

    return pd.DataFrame(data)

@pytest.fixture
def auto_file():
    data = {'Provider Name': ['Car R Us', 'AutoGuard', 'WeProtect', 'CarsOnly', 'Cars4U'],
            'CampaignID': ['AUTO1', 'AUTO2', 'AUTO3', 'AUTO4', 'AUTO5'],
            'Cost Per Ad Click': [5, "15", 32, 3, 5], 
            'Redirect Link': ['carrus.com', 'autoguard.net', 'weprotect.com', 'carsonly.com', 'cars4u.net'],
            'Phone Number': [1234567, 1234567, 1234567, 1125189, 1234567],
            'Address': ["123 A Street", "234 B Street", "354 D Street", "789 E Street", "345 C Street"], 
            'Zipcode': ["12345", "12343", "54321", "12345", "12354"],
            'Test Column': ['test', 'test', 'test', 'test', 'test'],
            'Account Id': [2, 1, 3, 4, 5]}
    return pd.DataFrame(data)
    

def test_file_collection(file_combiner, home_file):
    """Check that only CSV files have been collected."""
    file_combiner.files = [file for file in os.listdir('input_test')]
    file_dfs = file_combiner.collect_files(file_combiner.files)

    assert len(file_dfs) == 2

def test_required_cols(file_combiner, home_file):
    """Check that all required columns have remained after formatting"""
    formatted_dfs = file_combiner.format_files([home_file])
    required_cols = ['Provider Name','CampaignID', 'Cost Per Ad Click', 'Redirect Link', 'Phone Number', 'Address', 'Zipcode']

    for df in formatted_dfs:
        assert all(cols in df.columns.values for cols in required_cols)

def test_null_cols(file_combiner, home_file, auto_file):
    """Check that non-nullable columns all contain data."""
    formatted_dfs = file_combiner.format_files([home_file, auto_file])
    required_cols = ['Provider Name','CampaignID', 'Cost Per Ad Click', 'Redirect Link', 'Address', 'Zipcode']

    for df in formatted_dfs:
        df = df[df[required_cols].isnull().any(axis=1)]
        assert df.empty

def test_schema(file_combiner, home_file, auto_file):
    """Check that all columns contain the correct data types."""
    formatted_dfs = file_combiner.format_files([home_file, auto_file])

    types_dict = {'Provider Name': str,
                        'CampaignID': str,
                        'Cost Per Ad Click': float, 
                        'Redirect Link': str,
                        'Phone Number': str,
                        'Address': str, 
                        'Zipcode': str}

    # since strings are object types in Pandas, checking the actual values of the column to see if they fit they schema
    for df in formatted_dfs:
        for col, coltype in types_dict.items():

            vals = df[col].tolist()
            valcheck = [type(val) for val in vals]
            assert set(valcheck) == {coltype}