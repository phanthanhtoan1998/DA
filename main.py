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



# files = os.path.join("phongtro*.csv")
#
# # list of merged files returned
# files = glob.glob(files)
#
# df = pd.concat(map(pd.read_csv, files), ignore_index=True)
#
# print("The initial length of the dataset is", str(len(df)), "rows.")
#
#
# # #Kiểm tra dữ liệu bị missing values
# for col in df.columns:
#     missing_data = df[col].isna().sum()
#     missing_percent = missing_data/len(df) * 100
#     print(f"Column {col}:has { missing_percent} %")
# # p = msno.bar(df)
# # plt.show()
#
# # format data
# # df['Price'] = df['Price'].str.replace('triệu/tháng','').str.strip()
# df['District'] = df['District'].str.replace('Quận','').str.strip()
# df['Ward'] = df['Ward'].str.replace('Phường','').str.strip()
# df['Area'] = df['Area'].str.replace('m2','').str.strip().astype(float)
#
# df.loc[df['Price'].str.contains('triệu/tháng', na=False), 'Price'] = df.loc[df['Price'].str.contains('triệu/tháng', na=False), 'Price'].str.replace(' ','').str.replace('triệu/tháng','').str.replace(',','.').astype(float) *1000000
# df.loc[df['Price'].str.contains('trăm/tháng', na=False), 'Price'] = df.loc[df['Price'].str.contains('trăm/tháng', na=False), 'Price'].str.replace(' ','').str.replace('trăm/tháng','').str.replace(',','.').astype(float)*100000
# df.loc[df['Price'].str.contains('đồng/tháng', na=False), 'Price'] = df.loc[df['Price'].str.contains('đồng/tháng', na=False), 'Price'].str.replace(' ','').str.replace('đồng/tháng','').str.replace(',','.').astype(float)
#
# times = df['Time'].str.split("/")
#
# month = []
# year = []
#
# for time in times:
#     month.append(time[1])
#     year.append(time[2])
#
# df['Month'] = month
# df['Year'] = year
#
#
# # Create dummies for categorical columns
# dummy_district = pd.get_dummies(df.District, prefix="District")
# dummy_ward = pd.get_dummies(df.Ward, prefix="Ward")
# dummy_month = pd.get_dummies(df.Month, prefix="Month")
# dummy_year = pd.get_dummies(df.Year, prefix="Year")
#
#
# df_cleaned = pd.concat([df, dummy_district, dummy_ward, dummy_month, dummy_year], axis=1)
# df_cleaned = df_cleaned.drop(['District', 'Ward', 'Time', 'Month', 'Year'], axis=1)

# export_csv = df_cleaned.to_csv(r'data.csv', index = None, header=True)
df = pd.read_csv("data.csv")

def remove_outlier_IQR(df, series):
    Q1 = df[series].quantile(0.25)
    Q3 = df[series].quantile(0.75)
    IQR = Q3 - Q1
    df_final = df[~((df[series] < (Q1 - 1.5 * IQR)) | (df[series] > (Q3 + 1.5 * IQR)))]
    return df_final

removed_outliers = df
columns_to_remove_outliers = ['Price', 'Area']
for column in columns_to_remove_outliers:
    removed_outliers = remove_outlier_IQR(removed_outliers, column)

print("The final length of the dataset is", str(len(removed_outliers)), "rows.")
housing = removed_outliers

# Separate predictors and response (price) variables
X = housing.loc[:, housing.columns != 'Price']
y = housing[['Price']]
to_be_scaled = ['num_floors', 'num_bed_rooms', 'squared_meter_area', 'length_meter', 'width_meter']

X_array = np.array(X.values).astype("float32")
y_array = np.array(y).astype("float32")

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X_array, y_array, test_size=0.2, random_state=0)

from sklearn.ensemble import RandomForestRegressor
regr = RandomForestRegressor(max_depth=2, random_state=0)
regr.fit(X_train, np.ravel(y_train, order='C'))

# reult = regr.predict(X_test)
print(regr.score(X_test, y_test))
# print(np.min(reult, axis=0))
# print(np.max(reult, axis=0))

from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
regr = SVR(C=1.0, epsilon=0.2)
regr.fit(X_train, np.ravel(y_train))
# reult = regr.predict(X_test)

print(regr.score(X_test, y_test))
# print(np.min(reult, axis=0))
# print(np.max(reult, axis=0))

from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(X_train, y_train)
kq = lm.predict(X_test)
print(lm.score(X_test, y_test))