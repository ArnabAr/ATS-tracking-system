import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey there! Imagine yourself as a highly skilled ATS (Applicant Tracking System) engineer with expertise
 in various technical domains including software engineering, data science, data analytics, and big data engineering.
 Your mission is to develop an advanced ATS tracking system that effectively evaluates resumes based on given job descriptions. 
 Keep in mind the fiercely competitive job market, and strive to provide top-notch assistance to candidates in improving their 
 resumes.

Here's what you need to achieve:

1. Evaluate resumes based on the provided job description.
2. Assign a percentage match based on the job description.
3. Identify missing keywords with high accuracy.
4. Provide insightful profile summaries to assist candidates in enhancing their resumes.

Your system should streamline the hiring process, enhance candidate screening, and improve overall recruitment efficiency.

Please provide the response in a single string with the following structure:
{"JD Match": "%",  
"MissingKeywords": [],  
"Profile Summary": ""}
"""

## streamlit app
st.markdown(
"""
<style>
    .reportview-container {
        background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(120deg, #2980B9 0%, #6DD5FA 100%);
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #F0F3F4;
        color: black;
    }
    .stTextInput>label {
        color: black;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Smart ATS")
st.markdown("### Improve Your Resume with ATS")
jd = st.text_area("Paste the Job Description", height=200)
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Please upload the PDF")

# Submit button
submit = st.button("Submit")

# Handle submission
if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        response_json = json.loads(response)

        st.markdown("---")
        st.subheader("Response:")
        st.markdown(f"- **JD Match:** {response_json['JD Match']}")
        st.markdown(f"- **Missing Keywords:** {', '.join(response_json['MissingKeywords'])}")
        st.markdown(f"- **Profile Summary:** {response_json['Profile Summary']}")