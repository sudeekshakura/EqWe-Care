#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 00:26:18 2024

@author: sudeekshakura

"""
#pip install "pymongo[srv]"

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 
import time # for simulating a real-time data, time loop          
import numpy as np # np mean, np random             
import plotly.express as px # interactive charts  
import seaborn as sns
from statsmodels.graphics.mosaicplot import mosaic
import squarify
import matplotlib

uri = "mongodb+srv://kura:Elnino123456789@cluster0.afwuy4j.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)            


db = client.Gtech
collection = db.Gtech
data = pd.DataFrame(list(collection.find()))



st.set_page_config   (                     
page_title ="Patient EHR Dashboard",           
page_icon ="Active",          
layout ="wide",       
)

# dashboard title
st.title("Real-Time EqWe Care Dashboard")

def age_status(age):
    if age<2:
        return('Babies')
    elif (age<16 and age>=3):
        return('Children') 
    elif (age<30 and age>=17):
        return('Young Adults')
    elif (age<45 and age>=31):
        return('Middle-Aged Adults')
    else: 
        return('Old Adults')

def bmi_category(bmi):
    if bmi<18.5:
        return('Underweight')
    elif (bmi>=18.5 and bmi<25):
        return('Normal') 
    elif (bmi>=25 and bmi<30):
        return('Overweight')
    elif (bmi<35 and bmi>=30):
        return('Obesity first Class')
    elif (bmi<40 and bmi>=35):
        return('Obesity second Class')
    else: 
        return('Obesity third Class')

data['age_status']=data['age'].apply(age_status)
data['bmi_category']=data['bmi'].apply(bmi_category)
data_dict_list={1:'Yes',2:'No'}
data['cancer']=data['cancer'].map(data_dict_list)
data['smoker']=data['smoker'].map(data_dict_list)
data['insurance']=data['insurance'].map(data_dict_list)
data_1 = pd.crosstab(data['smoker'], data['cancer'])
data_1=data.groupby([data['cancer'], data['smoker']])['seqn'].count().to_frame().reset_index()
data_dict_list_2={1:'Excellent',2:'Good',3:'Average',4:'Bad',5:'Poor'}
data['gen_health']=data['gen_health'].map(data_dict_list_2)
data_2=data.groupby([data['gen_health'], data['insurance']])['seqn'].count().to_frame().reset_index()
data_3=data.groupby([data['gen_health'], data['bmi_category'],data['gender']])['seqn'].count().to_frame().reset_index()
data_4=data.groupby(data['age_status'])['seqn'].count().to_frame().reset_index()
patients=data['seqn'].nunique()  
Metrics=len(data.columns)-15
insured_patients=data.query('insurance=="Yes"')
insured_patients=len(insured_patients)
medicare_patients=data.query('medicare==1')
medicare_patients=len(medicare_patients)
       

# top-level filters
#streamlit function
def main():
    global data
    #age_filter = st.selectbox("Select the age group", pd.unique(data["age_status"]))

# creating a single-element container
    #placeholder = st.empty()

# dataframe filter
    
    #data = data[data["age_status"] == age_filter]


# create columns 
    dash_1 = st.container() 
    with dash_1:            
        kpi1, kpi2,kpi3,kpi4 = st.columns(4)  
        kpi1.metric("Number of Patients",round(patients),1)              
        
        kpi2.metric("Number of Evaluative Metrics",int(Metrics),delta =  10)               
        kpi3.metric("Number of Insured Patients",insured_patients,delta = 10)
        kpi4.metric("Number of Medicared Patients",medicare_patients,delta = 10)              
          


    # fill the column with respect to the KPIs 
    fig = plt.figure(figsize=(5,4))
    
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown("### Cancer diagnosis vs Smoking Habits")
        mosaic(data_1,['smoker','cancer'])
        st.pyplot(plt.gcf())
    plt.clf()
      
    with fig_col2:
        st.markdown("### Does Insurance show improved general health?")
        sns.barplot(data=data_2,x='seqn',y='insurance',hue='gen_health')
        st.pyplot(plt.gcf())
    plt.clf()
        
    fig_col_11, fig_col_12 = st.columns(2)
    with fig_col_11:
        st.markdown("### Does BMI impact general health?")
        fig_3=sns.FacetGrid(data_3,col='bmi_category',hue='gender',col_wrap=2)
        fig_3.map(sns.barplot,"gen_health","seqn")
        st.pyplot(fig_3.fig)
    plt.clf()
    with fig_col_12:
        st.markdown("### Patient Age Contibution")
        plt.pie(data_4['seqn'], labels = data_4['age_status'], autopct= '%.1f%%')
        st.pyplot(plt.gcf())
    time.sleep(1)
    

if __name__=='__main__':
    main()		
    
