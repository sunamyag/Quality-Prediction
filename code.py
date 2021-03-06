# -*- coding: utf-8 -*-
"""Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qTflk0zUILuPQ4qULIdZjw4QRcW2U6uO
"""

from google.colab import drive
drive.mount('/content/drive')

"""#IMPORTING the Libraries and Reading the Data"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('/content/drive/My Drive/Colab Notebooks/MiningProcess_Flotation_Plant_Database.csv', decimal=',', parse_dates=['date'],infer_datetime_format=True).drop_duplicates()
df['date'] = pd.to_datetime(df['date'])
df.head(10)

import matplotlib.style as style
# style.available

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd

"""# Exploratory Data Analysis"""

df.shape #To get the dimensions of data

df.isna().sum() #No missing Data

"""**Hence there is no missing data**"""

df.info()

"""**All Variable are numerical except the Date, No categorical data is present**"""

df.describe()

"""**Heat Map Correlation** """

plt.figure(figsize=(30, 25))
p = sns.heatmap(df.corr(), annot=True, cmap = 'coolwarm')

df = df.drop(['Flotation Column 01 Air Flow', 'Flotation Column 02 Air Flow', 'Flotation Column 07 Air Flow'], axis=1)  
df.shape

df.head(5)

"""**BOXPLOTS for Outlier Analysis**"""

columns = list(df.columns)
columns = columns[1:]

len(columns)

style.use('seaborn-paper') #sets the size of the charts
style.use('ggplot')

a = 4  # number of rows
b = 5  # number of columns
c = 1  # initialize plot counter
sns.set_context('paper')
fig = plt.figure(figsize=(36,18))

for i in range(len(columns)):
    plt.subplot(a, b, c)
    #plt.title('{}, subplot: {}{}{}'.format(i, a, b, c))
    plt.xlabel(i)
    sns.boxplot(x=df[columns[i]],orient="h", palette="Set2", color='cyan')
    c = c + 1

plt.show()

# for i in df.columns:
#     if(i=='date'):
#         continue
#     plt.figure(figsize=(16, 12))
#     sns.distplot(df[i])
#     plt.title(i)

"""**TimeSeries Plots of every attribute**"""

# for i in df.columns:
#   plt.figure(figsize=(20,5),dpi=100)
#   sns.scatterplot(x=df['date'],y=df[i])
#   plt.title(i)

"""**RANDOM SAMPLING FOR DISTRIBUTION ANALYSIS**"""

df1 = df.sample(frac=0.25, replace=True, random_state=1) #Random Sampling for distribution analysis

df1.shape

"""**Distribution Plots of the randomly sampled Data**"""

a = 4  # number of rows
b = 5  # number of columns
c = 1  # initialize plot counter
sns.set_context('paper')
fig = plt.figure(figsize=(36,18))

for i in df1.columns:
    if(i=='date'):
      continue
    plt.subplot(a, b, c)
    #plt.title('{}, subplot: {}{}{}'.format(i, a, b, c))
    plt.xlabel(i)
    sns.distplot(x=df1[i])
    c = c + 1

plt.show()

"""**Scatter Plots of % Silica Concentrate(Target Variable) with every variable**"""

# for i in df1.columns:
#     if(i=='date'):
#         continue
#     plt.figure(figsize=(20,5),dpi=100)
#     sns.scatterplot(x=df1[i],y=df1['% Silica Concentrate'])
#     plt.title(i)

a = 4  # number of rows
b = 5  # number of columns
c = 1  # initialize plot counter
sns.set_context('paper')
fig = plt.figure(figsize=(36,18),dpi=100)

for i in df1.columns:
    if(i=='date'):
      continue
    plt.subplot(a, b, c)
    #plt.title('{}, subplot: {}{}{}'.format(i, a, b, c))
    #plt.xlabel(i)
    sns.scatterplot(x=df1[i],y=df1['% Silica Concentrate'])
    #plt.title(i)
    c = c + 1

plt.show()

"""## Pre-Processing"""

df = df.drop(['date','% Iron Concentrate'], axis=1) #date is not relevant to the target that is the % Silica Concentrate
df.head(1)

df.shape

df.skew()

skewness = df.skew()

plt.figure(figsize=(8, 4))
sorted_idx = skewness.argsort()
plt.barh(df.columns[sorted_idx], skewness[sorted_idx])
plt.xlabel("Skewness")
plt.title("Feature wise skewness")

# remove outlier
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
#df2=df.drop(['date'],axis=1)
df_out = df[~((df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))).any(axis=1)]
df_out.shape

df_out.skew() #skewness of data after removing outlier

"""**Min-Max Normalization**"""

df_norm = df_out.copy()
for column in df_norm.columns:
        df_norm[column] = (df_norm[column] - df_norm[column].min()) / (df_norm[column].max() - df_norm[column].min())
df_norm.head(5)

# after removing outlier apply random sampling
df_new = df_norm.sample(frac=0.25, replace=True, random_state=1)
df_new.shape
# now data has only 133043 rows and we have already droped date columns

# for i in df_new.columns:
#     plt.figure(figsize=(16, 12))
#     sns.distplot(df_new[i])
#     plt.title(i)

#df1 = df.sample(frac=0.25, replace=True, random_state=1) #Random Sampling
Y = df_norm['% Silica Concentrate'] #Target Variable as per Kaggle
X = df_norm.drop(['% Silica Concentrate'], axis=1)
# X = X.drop(['date'], axis=1) #Date is useless

X.head()

Y.head()

"""##Modelling

"""

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.4, random_state=0,shuffle=True)

"""**Method for Linear Regression**"""

def LinearReg(X_train, X_test, y_train, y_test):
  model = LinearRegression()
  model.fit(X_train, y_train)
  print("Training error=",r2_score(y_train,model.predict(X_train)))
  print("R2 score=",r2_score(y_test,model.predict(X_test)))
  print("RMSE=",mean_squared_error(y_test,model.predict(X_test), squared=False))
  importance = model.coef_
  # summarize feature importance
  for i,v in enumerate(importance):
    print('Feature: %s, Score: %.5f' % (X_train.columns[i],v))
  # plot feature importance
  plt.bar([x for x in range(len(importance))], importance)
  plt.show()

"""
**Method for XGBoost Regression**

"""

def XGBreg(X_train, X_test, y_train, y_test):
  model = XGBRegressor()
  model.fit(X_train, y_train)
  print("Training error=",r2_score(y_train,model.predict(X_train)))
  print("R2 score=",r2_score(y_test,model.predict(X_test)))
  print("RMSE=",mean_squared_error(y_test,model.predict(X_test), squared=False))
  importance = model.feature_importances_
  # summarize feature importance
  for i,v in enumerate(importance):
    print('Feature: %s, Score: %.5f' % (X_train.columns[i],v))
  # plot feature importance
  plt.bar([x for x in range(len(importance))], importance)
  plt.show()

"""**Method for Random Forest Regression**"""

def RandomForestReg(X_train, X_test, y_train, y_test, num):
  model = RandomForestRegressor(n_estimators = num, random_state = 0)
  model.fit(X_train, y_train)
  print("Training error=",r2_score(y_train,model.predict(X_train)))
  print("R2 score=",r2_score(y_test,model.predict(X_test)))
  print("RMSE=",mean_squared_error(y_test,model.predict(X_test), squared=False))
  importance = model.feature_importances_
  # summarize feature importance
  for i,v in enumerate(importance):
    print('Feature: %s, Score: %.5f' % (X_train.columns[i],v))
  # plot feature importance
  plt.bar([x for x in range(len(importance))], importance)
  plt.show()

"""**Method for AdaBoost Regression**"""

def AdaBoostReg(X_train, X_test, y_train, y_test,num):
  from sklearn.ensemble import AdaBoostRegressor
  from sklearn.datasets import make_regression
  from sklearn.metrics import r2_score
  model = AdaBoostRegressor(base_estimator=DecisionTreeRegressor(), random_state=0, n_estimators=num)
  # model = AdaBoostRegressor()
  model.fit(X_train, y_train)
  print("Training error=",r2_score(y_train,model.predict(X_train)))
  print("R2 score=",r2_score(y_test,model.predict(X_test)))
  print("RMSE=",mean_squared_error(y_test,model.predict(X_test), squared=False))
  importance = model.feature_importances_
  # summarize feature importance
  for i,v in enumerate(importance):
    print('Feature: %s, Score: %.5f' % (X_train.columns[i],v))
  # plot feature importance
  plt.bar([x for x in range(len(importance))], importance)
  plt.show()

LinearReg(X_train, X_test, y_train, y_test)

XGBreg(X_train, X_test, y_train, y_test)

RandomForestReg(X_train, X_test, y_train, y_test,5)

AdaBoostReg(X_train, X_test, y_train, y_test,5)

"""## PCA



"""

from sklearn.decomposition import PCA
# Make an instance of the Model
pca = PCA(.95)

principalComponents = pca.fit_transform(X)

pca.n_components_

principalDf = pd.DataFrame(data = principalComponents
             , columns = [str(i) for i in range(1,pca.n_components_+1)])

pca_evr = pca.explained_variance_ratio_

pca_evr

"""Calculating the cumulative explained variance

"""

cum_explained_var = []
for i in range(0, len(pca_evr)):
    if i == 0:
        cum_explained_var.append(pca_evr[i])
    else:
        cum_explained_var.append(pca_evr[i] + 
                                 cum_explained_var[i-1])

plt.plot(cum_explained_var)
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')

principalDf.head(5)

X_train, X_test, y_train, y_test = train_test_split(principalDf, Y, test_size=0.4, random_state=0,shuffle=True)

"""**Modelling on PCA components**"""

LinearReg(X_train, X_test, y_train, y_test)

XGBreg(X_train, X_test, y_train, y_test)

RandomForestReg(X_train, X_test, y_train, y_test,50)

AdaBoostReg(X_train, X_test, y_train, y_test,50)

