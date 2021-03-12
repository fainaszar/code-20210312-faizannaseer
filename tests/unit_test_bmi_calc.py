import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bmi_calculator import calculate_bmi , calculate_bmi_risk_and_category


@pytest.fixture
def patient_data():
    return [{
    "Gender": "Female",
    "Height": 119,
    "Weight": 144,
    "BMI": 121.00840336134455,
    "Category": "Very Severely Obese",
    "Risk": "Very High Risk"
},
{
    "Gender": "Male",
    "Height": 295,
    "Weight": 182,
    "BMI": 61.69491525423729,
    "Category": "Very Severely Obese",
    "Risk": "Very High Risk"
},
{
    "Gender": "Female",
    "Height": 276,
    "Weight": 33,
    "BMI": 11.956521739130435,
    "Category": "Underweight",
    "Risk": "Malnutrition Risk"
},
{
    "Gender": "Male",
    "Height": 272,
    "Weight": 54,
    "BMI": 19.852941176470587,
    "Category": "Normal Weight",
    "Risk": "Low Risk"
}
]

def test_calculate_bmi(patient_data):

    assert calculate_bmi(124, 33) == 26.612903225806452
    assert calculate_bmi(patient_data[0]["Height"], patient_data[0]["Weight"]) == patient_data[0]["BMI"]


def test_calculate_bmi_risk_and_category(patient_data):

    assert calculate_bmi_risk_and_category(26.612903225806452) == ('Overweight','Enhanced Risk')
    assert calculate_bmi_risk_and_category(44)[0] == 'Very Severely Obese'
    assert calculate_bmi_risk_and_category(23.55)[1] != ('Enhanced Risk')
    assert len(calculate_bmi_risk_and_category(38)) == 2
    assert calculate_bmi_risk_and_category(patient_data[2]["BMI"]) == (patient_data[2]["Category"], patient_data[2]["Risk"])
    assert calculate_bmi_risk_and_category(patient_data[3]["BMI"])[0] == patient_data[3]["Category"]
