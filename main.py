import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import docx

# 1. YOUR EXACT CREWAI IMPORTS
from crewai import Crew, Process 
from agents import ats_expert, resume_writer, cover_letter_crafter 
from tasks import analyze_resume_task, rewrite_resume_task, write_cover_letter_task

load_dotenv()

# Initialize the FastAPI app
app = FastAPI(title="ATS Resume Optimizer API")

# Configure CORS to allow the React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/optimize")
def optimize_resume(
    job_description: str = Form(...),
    resume: UploadFile = File(...)
):
    """
    Endpoint to receive a resume and job description, run the CrewAI optimization,
    and return the newly generated Word document.
    """
    # Save the uploaded file temporarily to the server
    temp_resume_path = f"temp_{resume.filename}"
    with open(temp_resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
        
    try:
        # 1. EXTRACT TEXT FROM THE UPLOADED DOCX
        doc = docx.Document(temp_resume_path)
        extracted_text = "\n".join([para.text for para in doc.paragraphs])

        # 2. ASSEMBLE AND KICK OFF YOUR CREW
        my_crew = Crew(
            agents=[ats_expert, resume_writer, cover_letter_crafter],
            tasks=[analyze_resume_task, rewrite_resume_task, write_cover_letter_task],
            process=Process.sequential,
            verbose=True
        )

        # 3. PASS THE EXTRACTED TEXT (Notice the key is now 'resume_text')
        my_crew.kickoff(inputs={
            'resume_text': extracted_text, 
            'job_description': job_description
        })
        
        # The file your CrewAI script generates
        output_filename = "Optimized_Application.docx"
        
        # Return the generated Word document to the client
        return FileResponse(
            path=output_filename, 
            filename=output_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    finally:
        # Clean up the temporary uploaded file to save server space
        if os.path.exists(temp_resume_path):
            os.remove(temp_resume_path)