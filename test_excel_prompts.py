import pytest
import pandas as pd
from pipeline import answer_vlsi_query

# Load prompts and expected code from Excel
prompts = pd.read_excel("TestSet.xlsx", sheet_name="Prompt").iloc[:, 0]
expected_codes = pd.read_excel("TestSet.xlsx", sheet_name="Code").iloc[:, 0]

@pytest.mark.parametrize("query,expected", zip(prompts, expected_codes))
def test_from_excel(query, expected):
    resp = answer_vlsi_query(query)
    assert expected.strip() in resp 