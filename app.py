import streamlit as st
import requests
import json

def score_model(question):
    url = 'https://dbc-164e54c4-ef63.cloud.databricks.com/serving-endpoints/Final_Testing/invocations'
    headers = {'Authorization': f'Bearer {"dapi7aff94b92948d811e9f9019293f4705d"}', 'Content-Type': 'application/json'}
    data_json = {'inputs': [question]}
    response = requests.request(method='POST', headers=headers, url=url, data=json.dumps(data_json))
    if response.status_code != 200:
        raise Exception(f'Request failed with status {response.status_code}, {response.text}')
    return response.json()

st.title("Demo: Databricks model from Streamlit")
user_input = st.text_input("Ask your question")
if st.button("Send"):
    try:
        result = score_model(user_input)
        st.write("Result:")
        st.json(result) 
    except Exception as e:
        st.error(f"Error: {e}")
