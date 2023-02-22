import warnings
import numpy as np
import pandas as pd
import datetime
import seaborn as sns
# import matplotlib.pyplot as plt
import glob
import os
import matplotlib.pyplot as plt
import missingno as msno


files = os.path.join("phongtro*.csv")

# list of merged files returned
files = glob.glob(files)

df = pd.concat(map(pd.read_csv, files), ignore_index=True)

print("The initial length of the dataset is", str(len(df)), "rows.")


# #Kiểm tra dữ liệu bị missing values
for col in df.columns:
    missing_data = df[col].isna().sum()
    missing_percent = missing_data/len(df) * 100
    print(f"Column {col}:has { missing_percent} %")
# p = msno.bar(df)
# plt.show()

# format data
df['Price'] = df['Price'].str.replace('triệu/tháng','').str.strip()
df['District'] = df['District'].str.replace('Quận','').str.strip()
df['Ward'] = df['Ward'].str.replace('Phường','').str.strip()
df['Area'] = df['Area'].str.replace('m2','').str.strip()

# Create dummies for categorical columns
dummy_district = pd.get_dummies(df.District, prefix="District")
dummy_ward = pd.get_dummies(df.Ward, prefix="Ward")

df_cleaned = pd.concat([df, dummy_district, dummy_ward], axis=1)
df_cleaned = df_cleaned.drop(['District', 'Ward'], axis=1)

print(df_cleaned.head())

def remove_outlier_IQR(df, series):
    Q1 = df[series].quantile(0.25)
    Q3 = df[series].quantile(0.75)
    IQR = Q3 - Q1
    df_final = df[~((df[series] < (Q1 - 1.5 * IQR)) | (df[series] > (Q3 + 1.5 * IQR)))]
    return df_final