import os
from dotenv import load_dotenv
from crewai import Agent, LLM

# Load our API keys from the .env file
load_dotenv()

# We point CrewAI's native LLM wrapper to OpenRouter.
# Adding "openrouter/" to the model name tells LiteLLM exactly how to route it.
openrouter_llm = LLM(
    model="openrouter/google/gemini-2.5-flash",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ---------------------------------------------------------
# BUILD THE CREW
# ---------------------------------------------------------

# AGENT 1: The ATS Analyst
ats_expert = Agent(
    role="Senior ATS Optimization Specialist",
    goal="Analyze the user's resume against the job description to find missing keywords and formatting gaps.",
    backstory="You are a ruthless tech recruiter who uses Applicant Tracking Systems to filter out candidates. You know exactly what keywords algorithms look for.",
    llm=openrouter_llm,
    verbose=True # Prints the agent's thought process to the terminal
)

# AGENT 2: The Resume Writer
resume_writer = Agent(
    role="Executive Resume Writer",
    goal="Rewrite the resume bullet points to naturally integrate missing ATS keywords without inventing fake experience.",
    backstory="You are an elite career coach who specializes in taking existing career achievements and reframing them to perfectly match targeted job descriptions.",
    llm=openrouter_llm,
    verbose=True
)

# AGENT 3: The Cover Letter Crafter
cover_letter_crafter = Agent(
    role="Technical Copywriter",
    goal="Draft a highly personalized, compelling cover letter that connects the candidate's optimized resume to the company's specific needs.",
    backstory="You are a master storyteller who writes punchy, modern cover letters that bypass HR and get hiring managers excited.",
    llm=openrouter_llm,
    verbose=True
)