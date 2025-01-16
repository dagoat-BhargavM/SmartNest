import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load the dataset
data = pd.read_csv('/mnt/data/Synthetic_Indian_Demographic_Dataset.csv')

# Defining categorical and numerical columns
categorical_cols = ['Marital_Status', 'Educational_Level', 'Existing_Investments', 
                    'Financial_Goals', 'Employment_Status', 'Insurance_Coverage', 'Investment_Horizon']
numerical_cols = ['Age', 'Family_and_Dependents', 'Average_Monthly_Income', 'Average_Monthly_Expenses', 
                  'Savings_and_Emergency_Fund', 'Debt', 'Risk_Tolerance_Score']

# Preprocessing for numerical data
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine preprocessors in a column transformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Apply preprocessing
processed_data = preprocessor.fit_transform(data)

# Converting the preprocessed data back to a DataFrame
numerical_features = numerical_cols
categorical_features = preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(categorical_cols)
all_features = list(numerical_features) + list(categorical_features)
processed_df = pd.DataFrame(processed_data, columns=all_features)

# Save processed data to a new file
processed_df.to_csv('/mnt/data/Processed_Indian_Demographic_Dataset.csv', index=False)

print("Preprocessing and normalization complete. Processed data saved.")