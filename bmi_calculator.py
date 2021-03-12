import pandas as pd
from pandarallel import pandarallel
import simplejson
import argparse
import random

# Initialize Pandarallel to use multiprocessing, this is benificial when data is large.
pandarallel.initialize()


def load_random_data(size):
    """
        Generates random JSON LOV for testing purpose and loads into Pandas Dataframe

        param:: size: No of data points to be generated.
    """
    random_data = [{
        'Gender': random.choice(['Male', 'Female']),
        'HeightCm': random.randint(80, 300),
        'WeightKg': random.randint(30, 200)
    }
        for _ in range(size)]

    return pd.DataFrame(random_data)


def load_dataset(filename):
    """
        Reads JSON file data and loads it into pandas Dataframe

        param:: filename: Name of file to be read
    """
    try:
        data = simplejson.loads(open(filename, 'r').read())
    except FileNotFoundError as e:
        print(f"File {filename} not found. Plese specify a valid filename")
        exit()

    return pd.DataFrame(data)


def calculate_bmi(height, mass):
    """
        using height and mass, coverts height from Cm to m and then  calculates bmi value 

        param: height: It is the user height in Cms
        param: mass: It is the users weigth in Kgs
    """
    return mass/(height/100)


def calculate_bmi_risk_and_category(bmi):
    """
        Using the bmi value determines RISK and Category for BMI 

        param:: bmi : Users bmi (Body Mass Index)
    """

    if bmi <= 18.4:
        RISK = "Malnutrition Risk"
        CATEGORY = "Underweight"
    elif bmi >= 18.5 and bmi <= 24.9:
        RISK = "Low Risk"
        CATEGORY = "Normal Weight"
    elif bmi >= 25 and bmi <= 29.9:
        CATEGORY = "Overweight"
        RISK = "Enhanced Risk"
    elif bmi >= 30 and bmi <= 34.9:
        CATEGORY = "Moderately Obese"
        RISK = "Medium Risk"
    elif bmi >= 35 and bmi <= 39.9:
        CATEGORY = "Severely Obese"
        RISK = "High Risk"
    else:
        CATEGORY = "Very Severely Obese"
        RISK = "Very High Risk"

    return CATEGORY, RISK


if __name__ == "__main__":

    # Parse Arguments from commandline
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="JSON file to be loaded")
    group.add_argument("--size", help="Size of random data to be generated", type=int)
    arg = parser.parse_args()

    # Assuming only json format is supported
    
    if arg.file and not arg.file.endswith(".json"):
        print("Only files of type JSON, JSONL supported")
        exit()

    #If filename is not provided, uses size argument to load random data, else loads data from file , Raises error if neither of them is specified
    if arg.file:
        # Load data from file
        df = load_dataset(filename)
    else:

        # Load data generated randomly
        df = load_random_data(arg.size)

    # Calculate Body Mass Index in Kg/m2
    df["BmiKgm2"] = df.parallel_apply(
        lambda x: calculate_bmi(x.HeightCm, x.WeightKg), axis=1)

    # Determine Category and Risk level based on BMI Value
    df[["bmiCategory", "bmiRisk"]] = df.parallel_apply(
        lambda x: calculate_bmi_risk_and_category(x.BmiKgm2), axis=1, result_type="expand")

    # Save Processed Data into CSV files.
    print(df.head())
    df.to_csv("CalculatedValues.csv")
    print("Category Wise Report")
    print(df.bmiCategory.value_counts())
    df.bmiCategory.value_counts().to_csv("CategoryWiseReport.csv")

    print('\n*********\n')

    print("Gender Wise REPORT")
    print(df.groupby('Gender').bmiCategory.value_counts())
    df.groupby('Gender').bmiCategory.value_counts().to_csv(
        "GenderWiseBMIReport.csv")
