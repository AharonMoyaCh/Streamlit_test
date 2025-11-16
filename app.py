import streamlit as st
import requests
import json
import pandas as pd
from databricks import sql

SERVER_HOSTNAME = st.secrets["SERVER_HOSTNAME"]
HTTP_PATH = st.secrets["HTTP_PATH"]
ACCESS_TOKEN = st.secrets["ACCESS_TOKEN"]
url = st.secrets["URL"]

def get_query(question):
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}', 'Content-Type': 'application/json'}
    data_json = {'inputs': [question]}
    response = requests.request(method='POST', headers=headers, url=url, data=json.dumps(data_json))
    if response.status_code != 200:
        raise Exception(f'Request failed with status {response.status_code}, {response.text}')
    return response.json()
    
def clean_sql(sql_query):
    sql_upper = sql_query.upper()
    idx_with = sql_upper.find("WITH")
    idx_select = sql_upper.find("SELECT")
    idx = -1
    if idx_with != -1 and idx_select != -1:
        idx = min(idx_with, idx_select)
    elif idx_with != -1:
        idx = idx_with
    elif idx_select != -1:
        idx = idx_select
    
    if idx != -1:
        return sql_query[idx:] 
    else:
        return sql_query 

def run_query(sql_query):
    connection = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,  
        access_token=ACCESS_TOKEN
    )
    cursor = connection.cursor()
    cursor.execute(sql_query)
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return pd.DataFrame(data, columns=columns)

st.title("Demo: Databricks model from Streamlit")
user_input = st.text_input("Ask your question")
if st.button("Send"):
    try:
        result = get_query(user_input)
        sql_query = result['predictions'][0]['sql']
        data = run_query(clean_sql(sql_query))
        st.subheader("Generated SQL Query:")
        st.code(sql_query, language='sql')
        st.subheader("Query Result:")
        st.dataframe(data)
    except Exception as e:
        st.error(f"Error: {e}")
