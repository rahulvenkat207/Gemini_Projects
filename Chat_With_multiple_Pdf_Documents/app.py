import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter  
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##getting PDF
def get_pdf_text(pdf_docs):
    """To read and get the text from multiple documents by reading all the pages"""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

##Dividing into chunks
def get_text_chunks(text):
    """Splitting the text based on the RCT"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

##Converted into vectors
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide
    all the details. If the answer is not in the provided context, just say, "Answer is not available in the 
    context", don't provide the wrong answer.
    Context:\n{context}\n
    Question:\n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt) ##stuff- internal text summarization
    return chain

##user input 

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()
    
    response = chain(
        {
            "input_documents": docs, "question": user_question
        }, return_only_outputs=True)
    
    return response["output_text"]


   

def main():
    st.set_page_config(page_title="PDF QA Bot", page_icon="📄")
    
    st.title("PDF QA Bot")
    st.header("Upload PDF documents and ask questions")

    # Sidebar for uploading PDF documents
    st.sidebar.header("Upload PDF documents")
    uploaded_files = st.sidebar.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        with st.spinner("Processing..."):
            # Get text from PDFs and convert to vectors
            pdf_text = get_pdf_text(uploaded_files)
            text_chunks = get_text_chunks(pdf_text)
            get_vector_store(text_chunks)
            st.sidebar.success("PDFs processed successfully!")

    # User input for questions
    user_question = st.text_input("Ask a question about the PDFs:")
    if user_question:
        with st.spinner("Generating answer..."):
            response = user_input(user_question)
            st.write("Reply: ", response)

if __name__ == "__main__":
    main()
