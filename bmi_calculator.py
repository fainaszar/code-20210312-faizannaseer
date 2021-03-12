import pandas as pd
from pandarallel import pandarallel
import simplejson
import argparse
import random

pandarallel.initialize()


def load_random_data(size):
    random_data =  [{
        'Gender': random.choice(['Male','Female']),
        'HeightCm': random.randint(80,300),
        'WeightKg' : random.randint(30, 200)
    }
    for _ in range(size)]

    return pd.DataFrame(random_data)
    
def load_dataset(filename):

    data = simplejson.loads(open(filename,'r').read())
    return pd.DataFrame(data)



def calculate_bmi(height, mass):
    return mass/(height/100)


def calculate_bmi_risk_and_category(bmi):

    if bmi <= 18.4:
        RISK ="Malnutrition Risk"
        CATEGORY = "Underweight"
    elif bmi >= 18.5 and bmi <=24.9:
        RISK = "Low Risk"
        CATEGORY = "Normal Weight" 
    elif bmi >= 25 and bmi <=29.9:
        CATEGORY = "Overweight"
        RISK = "Enhanced Risk"
    elif bmi >= 30 and bmi <= 34.9:
        CATEGORY="Moderately Obese"
        RISK="Medium Risk"
    elif bmi >= 35 and bmi <= 39.9:
        CATEGORY="Severely Obese"
        RISK="High Risk"
    else:
        CATEGORY="Very Severely Obese"
        RISK = "Very High Risk"

    return CATEGORY, RISK

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="JSON file to be loaded", required=True)
arg = parser.parse_args()

filename = arg.file
if not filename.endswith(".json"):
    print("Only files of type JSON, JSONL supported")
    exit()

# df = load_dataset(filename)

df = load_random_data(100000)

df["BmiKgm2"] = df.parallel_apply(lambda x: calculate_bmi(x.HeightCm, x.WeightKg), axis=1) 

df[["bmiCategory","bmiRisk"]] = df.parallel_apply(lambda x: calculate_bmi_risk_and_category(x.BmiKgm2), axis=1, result_type="expand")

print(df.head())
df.to_csv("CalculatedValues.csv")
print("Category Wise Report")
print(df.bmiCategory.value_counts())
df.bmiCategory.value_counts().to_csv("CategoryWiseReport.csv")

print('\n*********\n')

print("Gender Wise REPORT")
print(df.groupby('Gender').bmiCategory.value_counts())
df.groupby('Gender').bmiCategory.value_counts().to_csv("GenderWiseBMIReport.csv")


