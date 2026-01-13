import streamlit as st
from openai import OpenAI
from docx import Document
from io import BytesIO
import textwrap

st.set_page_config(page_title="ATS Resume Optimizer", layout="centered")

st.title("ATS Resume Optimizer")
st.write("Upload your resume and paste the job description to generate an ATS-optimized resume and cover letter.")

from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    project=st.secrets["OPENAI_PROJECT_ID"]
)

resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
jd = st.text_area("Paste Job Description", height=250)

def generate_text(prompt):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return response.output_text 
    
def create_docx(text):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    bio = BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio

if st.button("Generate ATS Resume"):
    if not resume_file or not jd:
        st.warning("Please upload resume and paste job description.")
    else:
        with st.spinner("Optimizing your resume..."):
            resume_text = resume_file.read().decode(errors="ignore")

            resume_prompt = f"""
Rewrite this resume to match the job description.
Rules:
- Do not invent experience
- Preserve companies, roles, dates
- ATS friendly
- Single column
- Professional tone

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd}
"""

            cover_prompt = f"""
Write a professional cover letter tailored to this job.
Mention company and role.
3–4 short paragraphs.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd}
"""

            optimized_resume = generate_text(resume_prompt)
            cover_letter = generate_text(cover_prompt)

            resume_docx = create_docx(optimized_resume)
            cover_docx = create_docx(cover_letter)

        st.success("Done!")

        st.download_button(
            "⬇ Download ATS Resume (DOCX)",
            resume_docx,
            file_name="ATS_Resume.docx"
        )

        st.download_button(
            "⬇ Download Cover Letter (DOCX)",
            cover_docx,
            file_name="Cover_Letter.docx"
        )





