# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 11:20:54 2022

@author: ABHISHEK
"""

import numpy as np
from flask import Flask,request,jsonify,render_template
import requests

import json
API_KEY = "gh2T-jLLrC0Ers17AZJWqkLXBMrFurJExV5ix8D9hNd6"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
print("mltoken",mltoken)
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=Flask(__name__)
@app.route('/')
def home():
    return render_template("demo2.html")

@app.route('/y_predict',methods=['POST'])
def y_predict():
    
    gre=request.form["gre"]
    toefl=request.form["toefl"]
    rating=request.form["rating"]
    
    sop=request.form["sop"]
    lor=request.form["lor"]
    cgpa=request.form["cgpa"]
    research=request.form["research"]
    
    if(research=="0"):
        research=0
    if(research=="1"):
        research=1
    
    t=[[int(gre),int(toefl),float(rating),float(sop),float(cgpa),int(research)]]
    print(t)
    payload_scoring = {"input_data": [{"field": [["GRE Score","TOEFL Score","University Rating","SOP","LOR","CGPA","Research"]], "values": t}]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/245540f8-1433-430d-872f-725beceb8377/predictions?version=2022-06-18', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    predictions=response_scoring.json()
    print(predictions['predictions'][0]['values'][0][0])
    return render_template("Demo2.html",prediction_text=predictions['predictions'][0]['values'][0][1])
    
if __name__=="__main__":
    app.run(debug=True)
    

