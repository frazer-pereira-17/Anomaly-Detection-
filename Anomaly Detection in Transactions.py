#!/usr/bin/env python
# coding: utf-8

# ### Import Libraries

# In[1]:


import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report


# ### Reading the data

# In[2]:


data = pd.read_csv("C:/Users/FRAZER/Downloads/transaction_anomalies_dataset.csv")
print(data.head())


# ### Checking for NULL values

# In[3]:


print(data.isnull().sum())


# ### Getting data info

# In[4]:


print(data.info())


# ### Descriptive Statistics

# In[5]:


print(data.describe())


# ### Distribution of Transaction Amount

# In[6]:


fig_amount = px.histogram(data, x='Transaction_Amount',
                          nbins=20,
                          title='Distribution of Transaction Amount')
fig_amount.show()


# ### Transaction Amount by Account Type

# In[7]:


fig_box_amount = px.box(data,
                        x='Account_Type',
                        y='Transaction_Amount',
                        title='Transaction Amount by Account Type')
fig_box_amount.show()


# ### Average Transaction Amount vs. Age

# In[8]:


fig_scatter_avg_amount_age = px.scatter(data, x='Age',
                                        y='Average_Transaction_Amount',
                                        color='Account_Type',
                                        title='Average Transaction Amount vs. Age',
                                        trendline='ols')
fig_scatter_avg_amount_age.show()


# ### Count of Transactions by Day of the Week

# In[9]:


fig_day_of_week = px.bar(data, x='Day_of_Week',
                         title='Count of Transactions by Day of the Week')
fig_day_of_week.show()


# ### Correlation Heatmap

# In[10]:


correlation_matrix = data.corr()
fig_corr_heatmap = px.imshow(correlation_matrix,
                             title='Correlation Heatmap')
fig_corr_heatmap.show()


# ### Calculate mean and standard deviation of Transaction Amount

# In[11]:


mean_amount = data['Transaction_Amount'].mean()
std_amount = data['Transaction_Amount'].std()
print(mean_amount)
print(std_amount)


# ### Define the anomaly threshold (2 standard deviations from the mean)

# In[12]:


anomaly_threshold = mean_amount + 2 * std_amount
print(anomaly_threshold)


# ### Flag anomalies

# In[13]:


data['Is_Anomaly'] = data['Transaction_Amount'] > anomaly_threshold


# ### Scatter plot of Transaction Amount with anomalies highlighted

# In[14]:


fig_anomalies = px.scatter(data, x='Transaction_Amount', y='Average_Transaction_Amount',
                           color='Is_Anomaly', title='Anomalies in Transaction Amount')
fig_anomalies.update_traces(marker=dict(size=12), 
                            selector=dict(mode='markers', marker_size=1))
fig_anomalies.show()


# ### Calculate the number of anomalies

# In[15]:


num_anomalies = data['Is_Anomaly'].sum()


# ### Calculate the total number of instances in the dataset

# In[16]:


total_instances = data.shape[0]


# ### Calculate the ratio of anomalies

# In[17]:


anomaly_ratio = num_anomalies / total_instances
print(anomaly_ratio)


# # Training a Machine Learning model for Detecting Anomalies

# In[18]:


relevant_features = ['Transaction_Amount',
                     'Average_Transaction_Amount',
                     'Frequency_of_Transactions']


# ### Split data into features (X) and target variable (y)

# In[19]:


X = data[relevant_features]
y = data['Is_Anomaly']


# ### Split data into train and test sets

# In[20]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# ### Train the Isolation Forest model

# In[21]:


model = IsolationForest(contamination=0.02, random_state=42)
model.fit(X_train)


# ### Predict anomalies on the test set

# In[22]:


y_pred = model.predict(X_test)


# ### Convert predictions to binary values (0: normal, 1: anomaly)

# In[23]:


y_pred_binary = [1 if pred == -1 else 0 for pred in y_pred]


# ### Evaluate the model's performance

# In[24]:


report = classification_report(y_test, y_pred_binary, target_names=['Normal', 'Anomaly'])
print(report)


# ### Using trained model to detect anomalies

# In[30]:


# Relevant features used during training
relevant_features = ['Transaction_Amount', 'Average_Transaction_Amount', 'Frequency_of_Transactions']

# Get user inputs for features
user_inputs = []
for feature in relevant_features:
    user_input = float(input(f"Enter the value for '{feature}': "))
    user_inputs.append(user_input)

# Create a DataFrame from user inputs
user_df = pd.DataFrame([user_inputs], columns=relevant_features)

# Predict anomalies using the model
user_anomaly_pred = model.predict(user_df)

# Convert the prediction to binary value (0: normal, 1: anomaly)
user_anomaly_pred_binary = 1 if user_anomaly_pred == -1 else 0

if user_anomaly_pred_binary == 1:
    print("Anomaly detected: This transaction is flagged as an anomaly.")
else:
    print("No anomaly detected: This transaction is normal.")


# In[ ]:




