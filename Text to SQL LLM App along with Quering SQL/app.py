"""
Prompt -> LLm -> Gemini Pro -> Query ->SQL Database -> Response
Implementation
1. SqLlite -> insert some records-> python programming
2. LLM Apllicaiton -> Gemini pro-->sql Database
"""

import streamlit as st
from dotenv import load_dotenv
import sqlite3
import os
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini model and provide SQL query as response

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + "\n" + question)
    return response.text

## To retrieve query from the SQL database

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

## Define your prompt

prompt = """
You are an expert in converting English questions to SQL queries!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION

For example,
Example 1 - How many entries of records are present?, 
the SQL command will be something like this: SELECT COUNT(*) FROM STUDENT ;
Example 2 - Tell me all the students studying in Data Science class?, 
the SQL command will be something like this: SELECT * FROM STUDENT where CLASS="Data Science";
also the SQL code should not have ``` in the beginning or end and SQL word in output
"""

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.write(f"Generated SQL Query: {response}")
    
    try:
        data = read_sql_query(response, "student.db")
        st.subheader("The Response is")
        for row in data:
            st.write(row)
    except Exception as e:
        st.error(f"An error occurred: {e}")
