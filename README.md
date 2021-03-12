# code-20210312-faizannaseer

## BMI VALUE , CATEGORY and RISK LEVEL Calculator

A  script to calculate bmi values , category and risk level from a given set of data. The script make use of command line arguments --file and --size which are mutually 
exculive to be used when running. 

If **--file** parameter is specified, the script expects a JSON file, whose content is then loaded into pandas Dataframe
and the values are calculated accordingly

```python bmi_calculator.py --file filename.json```

If **--size** parameter is passed insteadm, the script generates random data of specified size and calculates values on them.

``` python bmi_calculator.py --size 10000```

If neither of the two params are specified, the script wont rum.
```
usage: bmi_calculator.py [-h] (--file FILE | --size SIZE)
bmi_calculator.py: error: one of the arguments --file --size is required

```

Successfull completion of scrip will result in displaying result for first 5 values, and counts for Each Category and  another one with data grouped by Gender.
```
   Gender  HeightCm  WeightKg    BmiKgm2          bmiCategory         bmiRisk
0  Female       209        68  32.535885     Moderately Obese     Medium Risk
1    Male       233       139  59.656652  Very Severely Obese  Very High Risk
2  Female       192        46  23.958333        Normal Weight        Low Risk
3  Female       255       125  49.019608  Very Severely Obese  Very High Risk
4  Female       159        99  62.264151  Very Severely Obese  Very High Risk
```

```
Category Wise Report
Very Severely Obese    72
Overweight              6
Normal Weight           6
Moderately Obese        6
Underweight             6
Severely Obese          4
```


```
Gender Wise REPORT
Gender  bmiCategory        
Female  Very Severely Obese    38
        Moderately Obese        4
        Normal Weight           4
        Underweight             2
        Overweight              1
        Severely Obese          1
Male    Very Severely Obese    34
        Overweight              5
        Underweight             4
        Severely Obese          3
        Moderately Obese        2
        Normal Weight           2
```

Also 3 files get generated which store this information, which can be used later.
* `CalculatedValues.csv` : Which stores all the processed data
* `CategoryWiseReport.csv`: Which stores category wise counts
* `GenderWiseBMIReport.csv`: Which stores category count based on Gender.


Tests are also privided which can be run using pytest.
