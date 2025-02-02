# -*- coding: utf-8 -*-
"""PDS_ASSIGNMENT2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/157tUfR2yWWWNDfWrh1r0rDVycg4-CAlG
"""

import pandas as pd
import numpy as np
import re
import datetime

"""Loading dataset

"""

data=pd.read_csv('/content/sample_data/train.csv')
data.head()

"""a) Look for the missing values in all the columns and either impute themm (replace with mean,
median, or mode) or drop them. Justify your action for this task. (4 points)

"""

missing_values = data.isnull().sum()
print("Missing Values:\n", missing_values)


def convert_mileage(x):
    try:
        return float(x.split()[0])
    except:
        return np.nan


data['Mileage'] = data['Mileage'].apply(convert_mileage)
data['Mileage'] = data['Mileage'].fillna(data['Mileage'].median())


for col in ['Engine', 'Power']:
    data[col] = data[col].astype(str).str.extract('(\d+\.?\d*)').astype(float)
    data[col] = data[col].fillna(data[col].median())


data['Seats'] = data['Seats'].fillna(data['Seats'].mode()[0])


data['New_Price_Missing'] = data['New_Price'].isnull().astype(int)
data['New_Price'] = pd.to_numeric(data['New_Price'], errors='coerce')
data['New_Price'] = data['New_Price'].fillna(data['New_Price'].median())


data['Year'] = pd.to_datetime(data['Year'], format='%Y')
data['Year'] = data['Year'].dt.strftime('%Y')



print(data.isnull().sum())



"""b) Remove the units from some of the attributes and only keep the numerical values (for
example remove kmpl from “Mileage”, CC from “Engine”, bhp from “Power”, and lakh from
“New_price”). (4 points)

"""

import pandas as pd
import re



def extract_numeric(value):
    if pd.isna(value):
        return value
    match = re.search(r'\d+(\.\d+)?', str(value))
    return float(match.group()) if match else None

columns_to_process = ['Mileage', 'Engine', 'Power', 'New_Price']

for column in columns_to_process:
    if column in data.columns:
        data[column] = data[column].apply(extract_numeric)
    else:
        print(f"Warning: Column '{column}' not found in the DataFrame.")

existing_columns = [col for col in columns_to_process if col in data.columns]
print(data[existing_columns].head())

"""C) Change the categorical variables (“Fuel_Type” and “Transmission”) into numerical one hot
encoded value. (4 points).
"""

data_encoded = pd.get_dummies(data, columns=['Fuel_Type', 'Transmission'], drop_first=True)

data_encoded.rename(columns={
    'Fuel_Type_Diesel': 'Fuel_Type_Diesel',
    'Fuel_Type_Petrol': 'Fuel_Type_Petrol',
    'Transmission_Manual': 'Transmission_Manual',
    'Transmission_Automatic': 'Transmission_Automatic'
}, inplace=True)


print(data_encoded)

"""d) Create one more feature and add this column to the dataset (you can use mutate function in
R for this). For example, you can calculate the current age of the car by subtracting “Year” value
from the current year. (4 points)

"""

print(data.dtypes)

data['Year'] = data['Year'].astype(int)
current_year = datetime.datetime.now().year
data['Car_Age'] = current_year - data['Year']
print(data[['Year', 'Car_Age']].head())

"""e) Perform select, filter, rename, mutate, arrange and summarize with group by operations (or
their equivalent operations in python) on this dataset. (4 points)
"""

import pandas as pd
import numpy as np


print("Available columns:")
print(data.columns)


data_selected = data[['Name', 'Year', 'Price', 'Kilometers_Driven']]

# 2. Filter (equivalent to filter() in R)
data_filtered = data[data['Year'] > 2015]

# 3. Rename (equivalent to rename() in R)
data_renamed = data.rename(columns={
    'Kilometers_Driven': 'Mileage'
})

# 4. Mutate (equivalent to mutate() in R)
data['Price_per_km'] = data['Price'] / data['Kilometers_Driven']

# 5. Arrange (equivalent to arrange() in R)
data_arranged = data.sort_values(by=['Year', 'Price'], ascending=[False, True])

# 6. Summarize with group by (equivalent to group_by() and summarize() in R)
summary = data.groupby('Year').agg({
    'Price': ['mean', 'median'],
    'Kilometers_Driven': 'mean',
    'Mileage': 'mean'
}).reset_index()

summary.columns = ['Year', 'Avg_Price', 'Median_Price', 'Avg_Kilometers', 'Avg_Mileage']


print("\nSelected DataFrame:")
print(data_selected.head())

print("\nFiltered DataFrame:")
print(data_filtered.head())

print("\nRenamed DataFrame:")
print(data_renamed.head())

print("\nMutated DataFrame (new column):")
print(data[['Name', 'Price', 'Kilometers_Driven', 'Price_per_km']].head())

print("\nArranged DataFrame:")
print(data_arranged.head())

print("\nSummary with Group By:")
print(summary.head())

cleaned_dataset_filename = 'cleaned_used_cars_dataset.csv'
data.to_csv(cleaned_dataset_filename, index=False)