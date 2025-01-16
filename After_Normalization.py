import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

# Load raw data
raw_data = pd.read_csv('Synthetic_Indian_Demographic_Dataset.csv')

# Initialize scaler and one-hot encoder
scaler = StandardScaler()
one_hot_encoder = OneHotEncoder(sparse=False)

# Normalize numerical columns
numerical_columns = [
    'Age', 'Family_and_Dependents', 'Average_Monthly_Income',
    'Average_Monthly_Expenses', 'Savings_and_Emergency_Fund', 'Debt', 'Risk_Tolerance_Score'
]
normalized_numerical = scaler.fit_transform(raw_data[numerical_columns])
normalized_numerical_df = pd.DataFrame(normalized_numerical, columns=numerical_columns)

# One-hot encode categorical columns
categorical_columns = [
    'Marital_Status', 'Educational_Level', 'Existing_Investments',
    'Financial_Goals', 'Employment_Status', 'Investment_Horizon'
]
encoded_categorical = one_hot_encoder.fit_transform(raw_data[categorical_columns])
categorical_columns_names = one_hot_encoder.get_feature_names_out(categorical_columns)
encoded_categorical_df = pd.DataFrame(encoded_categorical, columns=categorical_columns_names)

# Expand insurance coverage into separate binary columns
insurance_types = ['Health Insurance', 'Critical Illness Insurance',
                   'Personal Accident Insurance', 'Term Life Insurance']
expanded_insurance = pd.DataFrame(0, index=raw_data.index, columns=insurance_types)
for insurance in insurance_types:
    expanded_insurance[insurance] = raw_data['Insurance_Coverage'].str.contains(insurance).fillna(False).astype(int)

# Combine all processed columns
final_normalized_data = pd.concat([
    normalized_numerical_df, encoded_categorical_df, expanded_insurance
], axis=1)

# Save the normalized dataset
final_normalized_data.to_csv('Normalized_Dataset.csv', index=False)

print("Normalized dataset has been successfully generated and saved as 'Normalized_Dataset.csv'.")