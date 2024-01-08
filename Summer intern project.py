#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
data=pd.read_csv('insurance.csv')
data


# In[2]:


copydata=data.copy()
copydata


# In[3]:


copydata.info()


# In[4]:


copydata.dtypes


# In[5]:


copydata['sex']=copydata['sex'].map({'male':0,'female':1})
copydata['smoker']=copydata['smoker'].map({'yes':1,'no':0})
copydata['region']=copydata['region'].map({'northwest':0, 'northeast':1,'southeast':2,'southwest':3})
copydata


# In[6]:


copydata.dtypes


# In[7]:


copydata.describe()


# In[8]:


import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.countplot(x=data['sex'])


# In[9]:


sns.countplot(x=data['children'])


# In[10]:


sns.countplot(x=data['bmi'])


# In[11]:


sns.countplot(x=data['region'])


# In[12]:


sns.countplot(x=data['age'])


# In[13]:


sns.countplot(x=data['smoker'])


# In[14]:


#bivaraite analysis between output charges and input parameters
features = ['sex', 'children', 'smoker', 'region']
 
plt.subplots(figsize=(20, 10))
for i, col in enumerate(features):
    plt.subplot(2, 2, i + 1)
    copydata.groupby(col).mean()['charges'].plot.bar()
plt.show()


# In[15]:


sns.scatterplot(x=data['age'],y=data['charges'],hue=data['smoker'])


# In[16]:


sns.scatterplot(x=data['bmi'],y=data['charges'],hue=data['smoker'])


# In[17]:


sns.boxplot(copydata['age'])


# In[18]:


sns.boxplot(copydata['bmi'])


# In[19]:


percentile25=copydata['bmi'].quantile(0.25)
percentile75=copydata['bmi'].quantile(0.75)


# In[20]:


percentile25


# In[21]:


percentile75


# In[22]:


iqr=percentile75-percentile25
iqr


# In[23]:


lower=percentile25-1.5*iqr
lower


# In[24]:


higher=percentile75+iqr*1.5
higher


# In[25]:


copydata[copydata['bmi']<lower]


# In[26]:


copydata[copydata['bmi']>higher]


# In[27]:


newcopydata=copydata[copydata['bmi']<higher]
newcopydata


# In[28]:


newcopydata.shape


# In[29]:


import seaborn as sns
sns.boxplot(newcopydata['bmi'])


# In[30]:


#check the skewness of the data
newcopydata['bmi'].skew()


# In[31]:


newcopydata['age'].skew()


# In[32]:


newcopydata


# In[33]:


newcopydata.corr()


# In[34]:


sns.heatmap(data=newcopydata.corr(),annot=True)


# In[35]:


#linear regression model 
from sklearn.model_selection import train_test_split,cross_val_score
x=newcopydata.drop(['charges'],axis=1)
y=newcopydata[['charges']]
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)


# In[36]:


x_train


# In[37]:


x_test


# In[38]:


y_train


# In[39]:


y_test


# In[40]:


from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score
reg=LinearRegression()
reg.fit(x_train,y_train)


# In[41]:


y_pred=reg.predict(x_test)


# In[42]:


y_pred


# In[43]:


print(np.sqrt(mean_squared_error(y_test,y_pred)))
print(reg.score(x_train,y_train))
print(reg.score(x_test,y_test))
cvscore=cross_val_score(reg,x,y,cv=5)
print(cvscore.mean())


# In[44]:


from pickle import dump
dump(reg,open('insurancemodelf.pkl','wb'))


# In[45]:


new_data=pd.DataFrame({'age':19,'sex':'female','bmi':27.9,'children':0,'smoker':'yes','region':'southwest'},index=[0])
new_data['smoker']=new_data['smoker'].map({'yes':1,'no':0})
new_data['sex']=new_data['sex'].map({'male':0,'female':1})
new_data['region']=new_data['region'].map({'northwest':0,'northeast':1,'southwest':2,'southeast':3})

reg.predict(new_data)


# In[46]:


from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error ,r2_score
X = newcopydata.drop(['charges'], axis=1)  
Y= newcopydata['charges']


# In[47]:


from sklearn.ensemble import RandomForestRegressor
xtrain,xtest,ytrain,ytest=train_test_split(X,Y,test_size=0.2,random_state=42)


# In[48]:


xtest


# In[49]:


ytest


# In[50]:


rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)


# In[51]:


rf_regressor.fit(xtrain, ytrain)


# In[52]:


y_pred = rf_regressor.predict(xtest)
y_pred


# In[53]:


#print(r2_score(xtrain,ytrain))
print(rf_regressor.score(xtest,ytest))
print(rf_regressor.score(xtrain,ytrain))
print(cross_val_score(rf_regressor,X,Y,cv=5,).mean())


# In[54]:


from pickle import dump
dump(rf_regressor,open('insurancemodelf.pkl','wb'))


# In[55]:


new_data1=pd.DataFrame({'age':19,'sex':'female','bmi':27.9,'children':0,'smoker':'yes','region':'southwest'},index=[0])
new_data1['smoker']=new_data1['smoker'].map({'yes':1,'no':0})
new_data1['sex']=new_data1['sex'].map({'male':0,'female':1})
new_data1['region']=new_data1['region'].map({'northwest':0,'northeast':1,'southwest':2,'southeast':3})

rf_regressor.predict(new_data1)


# In[56]:


from sklearn.ensemble import GradientBoostingRegressor
X = newcopydata.drop(['charges'], axis=1)  
Y= newcopydata['charges']

x1train,x1test,y1train,y1test=train_test_split(X,Y,test_size=0.2,random_state=i)


# In[57]:


x1train


# In[58]:


y1train


# In[59]:


x1test


# In[60]:


y1test


# In[61]:


grad = GradientBoostingRegressor(
    loss='squared_error',  
    learning_rate=0.2,
    n_estimators=15,
    max_depth=5,
    random_state=42
)
grad


# In[62]:


grad.fit(x1train,y1train)
res=grad.predict(x1test)
res


# In[63]:


print(grad.score(x1test,y1test))
print(grad.score(x1train,y1train))
print(cross_val_score(grad,X,Y,cv=5).mean())


# In[64]:


from pickle import dump
dump(grad,open('insurancemodel.pkl','wb'))


# In[65]:


new_data1=pd.DataFrame({'age':19,'sex':'female','bmi':27.9,'children':0,'smoker':'yes','region':'southwest'},index=[0])
new_data1['smoker']=new_data1['smoker'].map({'yes':1,'no':0})
new_data1['sex']=new_data1['sex'].map({'male':0,'female':1})
new_data1['region']=new_data1['region'].map({'northwest':0,'northeast':1,'southwest':2,'southeast':3})

grad.predict(new_data1)


# In[69]:


# Import necessary libraries
import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('insurancemodel.pkl')

# Define the Streamlit app
def main():
    st.title('Health Insurance Prediction System')

    # Create input fields
    age = st.slider('Select Age', 18, 100, 25)
    bmi = st.number_input('Enter BMI', min_value=10.0, max_value=50.0, value=25.0)
    children = st.number_input('Number of Children', min_value=0, max_value=10, value=0)
    smoker = st.selectbox('Are you a smoker?', ('No', 'Yes'))
    sex = st.selectbox('Select Gender', ('Male', 'Female'))
    region = st.selectbox('Select Region', ('Northwest', 'Southwest', 'NorthEast', 'SouthWest'))

    # Convert categorical values to numerical
    sex = 1 if sex == 'Male' else 0
    smoker = 1 if smoker == 'Yes' else 0

    # Convert region to numerical using one-hot encoding
    region_columns = pd.get_dummies(pd.Series([region]), prefix='region')
    input_data = pd.DataFrame({'age': [age], 'bmi': [bmi], 'children': [children], 'sex': [sex], 'smoker': [smoker]})
    input_data = pd.concat([input_data, region_columns], axis=1)

    # Make prediction
    if st.button('Predict'):
        prediction = model.predict(input_data)
        st.success(f'The predicted insurance status is: {prediction[0]}')

# Run the app
if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:



