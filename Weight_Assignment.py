# Update the weights dictionary to match the exact column names in the dataset
final_weights_aligned = {
    'Savings_and_Emergency_Fund': 0.1531,
    'Average_Monthly_Income': 0.1224,
    'Financial_Goals_Capital Growth/Expansion': 0.1020,
    'Educational_Level_Doctorate': 0.1020,
    'Existing_Investments_Equities': 0.0816,
    'Investment_Horizon_Short': 0.0816,
    'Educational_Level_Postgraduate': 0.0714,
    'Existing_Investments_Mutual Funds': 0.0714,
    'Existing_Investments_Real Estate': 0.0714,
    'Existing_Investments_Gold': 0.0612,
    'Employment_Status_Regular Salary': 0.0612,
    'Risk_Tolerance_Score': 0.0612,
    'Financial_Goals_Wealth Preservation': 0.0510,
    'Educational_Level_Undergraduate': 0.0510,
    'Investment_Horizon_Medium': 0.0408,
    'Health Insurance': 0.0408,
    'Existing_Investments_Fixed Deposits': 0.0408,
    'Critical Illness Insurance': 0.0306,
    'Term Life Insurance': 0.0306,
    'Marital_Status_Single': 0.0306,
    'Employment_Status_Varying Salary': 0.0306,
    'Investment_Horizon_Long': 0.0204,
    'Educational_Level_High School': 0.0204,
    'Personal Accident Insurance': 0.0204,
    'Age': -0.0102,
    'Marital_Status_Married': -0.0204,
    'Family_and_Dependents': -0.0306,
    'Marital_Status_Divorced': -0.0306,
    'Employment_Status_Unemployed': -0.0510,
    'Average_Monthly_Expenses': -0.1020,
    'Debt': -0.2041
}



# Recalculate the risk score with all features and aligned weights
dataset['Risk_Score'] = sum(
    dataset[feature] * weight for feature, weight in final_weights_aligned.items()
)
