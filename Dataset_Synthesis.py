import pandas as pd
import random
import numpy as np
# Define the features and their potential value ranges or categories based on the document details
data_structure = {
    "Age": lambda: random.randint(18, 70),  # Age above 18
    "Marital_Status": lambda: random.choice(["Single", "Divorced", "Married"]),
    "Family_and_Dependents": lambda: random.randint(0, 10),  # Number of dependents
    "Educational_Level": lambda: random.choice(["High School", "Undergraduate", "Postgraduate", "Doctorate"]),
    "Average_Monthly_Income": lambda: random.randint(10000, 200000),  # INR
    "Average_Monthly_Expenses": lambda x: random.randint(int(x * 0.5), int(x * 1.2)),  # Expenses as a range of income
    "Existing_Investments": lambda: random.choice(["Gold", "Real Estate", "Equities", "Mutual Funds", "Fixed Deposits"]),
    "Financial_Goals": lambda: random.choice(["Wealth Preservation", "Capital Growth/Expansion"]),
    "Employment_Status": lambda: random.choice(["Regular Salary", "Varying Salary", "Unemployed"]),
    "Savings_and_Emergency_Fund": lambda: random.randint(0, 50) * 100000,  # INR in lakhs
    "Insurance_Coverage": lambda: random.sample(
        ["Health Insurance", "Term Life Insurance", "Medical Insurance", "Motor Insurance"], k=random.randint(1, 4)
    ),
    "Debt": lambda: random.randint(0, 20) * 100000,  # INR
    "Investment_Horizon": lambda: random.choice(["Short", "Medium", "Long"]),
    "Risk_Tolerance_Score": lambda: random.randint(8, 32)  # Summation score from questionnaire responses
}

# Generate 10000 data points
data = []
for _ in range(10000):
    row = {}
    for feature, generator in data_structure.items():
        if feature == "Average_Monthly_Expenses":
            row[feature] = generator(row["Average_Monthly_Income"])
        else:
            row[feature] = generator()
    data.append(row)

# Create DataFrame
df = pd.DataFrame(data)

# Clean Insurance_Coverage to convert lists into a consistent format
df["Insurance_Coverage"] = df["Insurance_Coverage"].apply(lambda x: ", ".join(x))

