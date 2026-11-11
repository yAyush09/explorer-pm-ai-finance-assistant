# model.py (Updated and Clean)
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Load and clean data
df = pd.read_excel("data/insurance_data.xlsx")
df.columns = df.columns.str.strip()

# Use correct target column name from dataset
target_column = "Insurance"  # The actual column name in your Excel file

if target_column not in df.columns:
    raise ValueError(f"Column '{target_column}' not found in dataset. Available columns: {', '.join(df.columns)}")

# Encode categorical data
le = LabelEncoder()
df['Occupation'] = le.fit_transform(df['Occupation'])

# Save label encoder
os.makedirs("saved_model", exist_ok=True)
joblib.dump(le, 'saved_model/label_encoder.pkl')

# Generate synthetic data
def generate_more_data(df, n_samples=100):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    new_rows = []

    for _ in range(n_samples):
        row = df.sample(1).iloc[0].copy()
        for col in numeric_cols:
            noise = np.random.normal(0, 0.05)
            row[col] = row[col] * (1 + noise)
        new_rows.append(row)

    return pd.DataFrame(new_rows)

# Augment data
df = pd.concat([df, generate_more_data(df, n_samples=100)], ignore_index=True)

# Split features and target
X = df.drop(columns=[target_column])
y = df[target_column]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save trained model
joblib.dump(model, 'saved_model/model.pkl')

print("✅ Model and label encoder saved successfully.")
