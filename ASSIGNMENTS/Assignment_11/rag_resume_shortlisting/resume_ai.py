from groq_client import groq_call

def resume_summary(resume_text):
    prompt = f"""
Create a short professional summary (3–4 lines) from this resume.

Resume:
{resume_text[:2500]}
"""
    return groq_call(prompt)

def resume_scoring(resume_text, job_desc):
    prompt = f"""
Compare resume with job description and return:

Score (0–100):
Skill Match Percentage:
Matching Skills (comma separated):
Short Justification (2 lines)

Resume:
{resume_text[:2000]}

Job Description:
{job_desc[:1500]}
"""
    return groq_call(prompt)
