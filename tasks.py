from crewai import Task
from agents import ats_expert, resume_writer, cover_letter_crafter

# TASK 1: The Analysis
# The {resume_text} and {job_description} variables act as placeholders.
# We will inject the actual Word document text into these slots from main.py.
analyze_resume_task = Task(
    description="""Compare the provided resume against the job description.
    Identify exactly which required skills and keywords are missing from the resume.
    
    Resume: {resume_text}
    Job Description: {job_description}""",
    expected_output="A list of missing keywords and a brief summary of how well the resume matches the job.",
    agent=ats_expert
)

# TASK 2: The Rewrite
rewrite_resume_task = Task(
    description="""Using the keyword gaps identified by the ATS Specialist, rewrite the bullet points from the provided resume.
    Do NOT invent new jobs or degrees. Only rephrase existing bullet points to include the missing keywords naturally.
    
    Base Resume: {resume_text}""",
    expected_output="A finalized, polished list of optimized resume bullet points.",
    agent=resume_writer
)

# TASK 3: The Cover Letter
write_cover_letter_task = Task(
    description="""Using the optimized resume data and the target job description, write a 3-paragraph cover letter.
    Make it confident, modern, and directly address the requirements in the job description.
    
    Job Description: {job_description}""",
    expected_output="A ready-to-send, professional cover letter.",
    agent=cover_letter_crafter
)