from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

## input - act as an invoice extractor
## prompt - fetch me the addressform the image like that
def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Corrected key name and added missing comma
                "data": bytes_data
            }
        ]
        return image_parts  # Return the image parts
    else:
        raise FileNotFoundError("No file uploaded")



st.set_page_config(page_title="MultiLanguage Invoice Extracter")

st.header("MultiLanguage Invoice Extracter")

input = st.text_input("Input Prompt : ",key="input")

uploaded_file = st.file_uploader("Choose an image of the invoice...",type= ["jpg","jpeg","png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image.",use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompts = """
  You are an expert in understanding invoices. We will upload as a image as invoice
  and you will have to answer any questions based on the uploaded invoice image
"""

##When submit is clicked
if submit:
    image_data  = input_image_details(uploaded_file) 

    response = get_gemini_response(input_prompts,image_data,input)
    st.header("The Response is:")
    st.write(response)
