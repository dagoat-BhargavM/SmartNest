# Update the weights dictionary to match the exact column names in the dataset
final_weights_aligned = {
    'Age': -0.01,
    'Family_and_Dependents': -0.03,
    'Average_Monthly_Income': 0.12,
    'Average_Monthly_Expenses': 0.10,
    'Savings_and_Emergency_Fund': 0.15,
    'Debt': 0.20,
    'Risk_Tolerance_Score': 0.06,
    'Health Insurance': 0.04,
    'Critical Illness Insurance': 0.03,
    'Personal Accident Insurance': 0.02,
    'Term Life Insurance': 0.03,
    'Marital_Status_Divorced': -0.03,
    'Marital_Status_Married': -0.02,
    'Marital_Status_Single': 0.03,
    'Educational_Level_Doctorate': 0.10,
    'Educational_Level_High School': 0.02,
    'Educational_Level_Postgraduate': 0.07,
    'Educational_Level_Undergraduate': 0.05,
    'Existing_Investments_Equities': 0.08,
    'Existing_Investments_Fixed Deposits': 0.04,
    'Existing_Investments_Gold': 0.06,
    'Existing_Investments_Mutual Funds': 0.07,
    'Existing_Investments_Real Estate': 0.07,
    'Financial_Goals_Capital Growth/Expansion': 0.10,
    'Financial_Goals_Wealth Preservation': 0.05,
    'Employment_Status_Regular Salary': 0.06,
    'Employment_Status_Unemployed': -0.05,
    'Employment_Status_Varying Salary': 0.03,
    'Investment_Horizon_Long': 0.02,
    'Investment_Horizon_Medium': 0.04,
    'Investment_Horizon_Short': 0.08,
}


# Recalculate the risk score with all features and aligned weights
dataset['Risk_Score'] = sum(
    dataset[feature] * weight for feature, weight in final_weights_aligned.items()
)