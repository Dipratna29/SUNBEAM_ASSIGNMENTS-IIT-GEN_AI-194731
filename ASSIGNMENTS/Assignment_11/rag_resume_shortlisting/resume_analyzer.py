from groq_client import call_groq

def analyze_resume(resume_text):
    prompt = f"""
Analyze this resume and return:
1. Professional summary
2. Top skills (bullets)
3. Experience highlights

Resume:
{resume_text[:3000]}
"""
    return call_groq(prompt)

def score_resume(resume_text, job_desc):
    prompt = f"""
Compare resume with job description and give:
- Match score (0-100)
- Short justification

Resume:
{resume_text[:2500]}

Job Description:
{job_desc[:1500]}
"""
    return call_groq(prompt)
