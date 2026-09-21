import os
import shutil
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from crewai import Crew, Process

# Import your agents and tasks from your other files
# (Adjust these import names if your files/variables are named differently)
from agents import ats_expert, resume_writer, cover_letter_crafter
from tasks import analyze_resume_task, rewrite_resume_task, write_cover_letter_task

app = FastAPI()

# --- CORS CONFIGURATION ---
# This allows your Vercel frontend to talk to this Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://atsresume-eight.vercel.app", 
        "http://localhost:5173" # For local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MAIN ENDPOINT ---
# Using 'def' instead of 'async def' so CrewAI runs in a background thread
@app.post("/api/optimize")
def optimize_resume(
    job_description: str = Form(...),
    resume: UploadFile = File(...)
):
    print(f"DEBUG: Request received! File: {resume.filename}")
    
    # 1. Save the uploaded resume temporarily so CrewAI can read it
    temp_resume_path = f"temp_{resume.filename}"
    with open(temp_resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
        
    try:
        # 2. Initialize the Crew
        print("DEBUG: Initializing CrewAI...")
        my_crew = Crew(
            agents=[ats_expert, resume_writer, cover_letter_crafter],
            tasks=[analyze_resume_task, rewrite_resume_task, write_cover_letter_task],
            process=Process.sequential,
            verbose=True
        )

        # 3. Run the AI process
        print("DEBUG: Starting CrewAI kickoff...")
        my_crew.kickoff(inputs={
            'resume_path': temp_resume_path,
            'job_description': job_description
        })
        
        # 4. Return the generated document
        output_filename = "Optimized_Application.docx"
        print("DEBUG: Process complete, sending file back to frontend!")
        
        return FileResponse(
            path=output_filename, 
            filename=output_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except Exception as e:
        # Catch and print any hidden crashes to the Render logs
        print(f"CRASH REPORT: {str(e)}") 
        raise e
        
    finally:
        # 5. Clean up the temporary uploaded resume so your server storage doesn't fill up
        if os.path.exists(temp_resume_path):
            os.remove(temp_resume_path)
            print(f"DEBUG: Cleaned up temporary file {temp_resume_path}")