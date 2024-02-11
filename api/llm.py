from openai import OpenAI

import os
import numpy as np
import pandas as pd

import json
import requests


with open("./config.json","r+") as f:
    config_json  = json.load(f)
    openai = OpenAI(api_key=config_json['OPEN_AI_KEY'])

class LLM:
    prompts = {"patient_info":"Write the summary for an patient. Below is the information about the patient. ",
               "title_generate":"Give me the title of just the below summary. Just the title. {CONTENT}",
               "briefer":"Give me a brief description for around 200 words about this patient below. {CONTENT}"}

    def __init__(self):
        self.config_json = config_json
        self.openai = openai

    def generate_summary_response(self,record):

        processed_text = self.process_record(record)

        # Fetching Name of the UML Diagram
        response = openai.chat.completions.create(
				model="gpt-3.5-turbo",
				messages=[{"role": "system", "content":self.prompts["patient_info"]+ processed_text}],
		)
        response = response.choices[0].message.content.lower()

        brief = self.return_brief_content(record)

        return response,brief
    
    def return_brief_content(self,content):
        processed_text = self.process_record(content)

        # Fetching Name of the UML Diagram
        response = openai.chat.completions.create(
				model="gpt-3.5-turbo",
				messages=[{"role": "system", "content":self.prompts["briefer"].format(CONTENT=processed_text)}],
		)
        response = response.choices[0].message.content.lower()

        return response


    
    def process_record(self,record):
        
        record_text = ""

        # Mapper
        df = pd.read_excel("./data/columns_mapper.xlsx")
        df = df[['NHANES code','header']]
        df_values = df.to_dict()
        
        for key,values in df_values.items():
            df_values[key] = list(values.values())

        # Fetching Basic columns
        gender_template = "Patient is a {GENDER}. "

        # Record
        record_text+= "Name of the patient is " + record['first'] + " " + record["last"]+ ". "
        record_text = record_text + gender_template.format(GENDER="Male" if record['gender'] == 0 else "Female")
        record_text =  record_text + "Age of the patient is " + str(record['age'])

        columns_to_be_taken = filter(lambda x: x.startswith("lb"),list(df_values.keys()))

        temp = "value of {COLUMN} is {VALUE}. "
        for column in columns_to_be_taken:
            inx = df_values['NHANES code'].index(column)
            record_text+=temp.format(COLUMN = df_values['header'][inx],VALUE = str(record[column]))

        return record_text
    

    def bot_trav_response(self,user_inp):

        url = "https://api-ares.traversaal.ai/live/predict"
        payload = { "query": ["EqWeCare is a data driven one stop solution to access a vast multitude of patient's electronic health records in pdf,png and text file formats through the efficent use of Large Language Models. It is considered provide more optimized solutions than its competitors in the market at an economical price. "+ user_inp] }
        
        headers = {
        "x-api-key": "ares_dc8e85310f5e7886d559c70a51d87c36846b63121136ac03037d6e17a2a2d157",
        "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        return json.loads(response.text)['data']['response_text']