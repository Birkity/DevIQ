from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
from typing import List, Dict
from pymongo import MongoClient
import openai
from transformers import pipeline
import os
import requests

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
STACK_OVERFLOW_API_KEY = os.getenv("STACK_OVERFLOW_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client.deviq
feedback_collection = db.feedback
recommendation_collection = db.recommendations

# Define request and response models
class ProjectRequest(BaseModel):
    project: str

class RecommendationResponse(BaseModel):
    stack: List[str]
    latest_trends: str

class TaskPrioritizationResponse(BaseModel):
    prioritized_tasks: List[str]

# Initialize NLP models
summarizer = pipeline("summarization", model="t5-base")

# Mock data for demonstration purposes
tech_stacks = {
    "web": ["React", "Node.js", "MongoDB"],
    "data": ["Python", "Pandas", "Scikit-learn"],
    "mobile": ["Flutter", "Firebase"]
}

latest_trends = "AI, Blockchain, Quantum Computing"

prioritized_tasks = [
    "Define project scope",
    "Research technology options",
    "Develop MVP",
    "Test and iterate"
]

# External API functions
def fetch_github_trends():
    headers = {"Authorization": f"token {GITHUB_API_TOKEN}"}
    response = requests.get("https://api.github.com/search/repositories?q=stars:>10000&sort=stars", headers=headers)
    return response.json()["items"][:5]  # Return top 5 trending repos

def fetch_stack_overflow_trends():
    response = requests.get(f"https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow&key={STACK_OVERFLOW_API_KEY}")
    return response.json()["items"][:5]  # Return top 5 trending tags

# Endpoint for tech stack recommendation
@app.post("/recommend", response_model=RecommendationResponse)
async def recommend_tech_stack(request: ProjectRequest):
    # Use OpenAI API to generate recommendations
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Recommend a tech stack for the following project: {request.project}",
        max_tokens=150
    )
    recommended_stack = response.choices[0].text.strip().split(", ")
    
    if not recommended_stack:
        raise HTTPException(status_code=404, detail="No recommendations found")
    
    # Fetch external data
    github_trends = fetch_github_trends()
    stack_overflow_trends = fetch_stack_overflow_trends()
    
    # Store recommendation in MongoDB
    recommendation_collection.insert_one({
        "project": request.project,
        "stack": recommended_stack,
        "github_trends": github_trends,
        "stack_overflow_trends": stack_overflow_trends
    })
    
    return RecommendationResponse(stack=recommended_stack, latest_trends=latest_trends)

# Endpoint for task prioritization
@app.post("/prioritize_tasks", response_model=TaskPrioritizationResponse)
async def prioritize_tasks(request: ProjectRequest):
    # Use NLP model to break down tasks
    summary = summarizer(request.project, max_length=50, min_length=25, do_sample=False)
    tasks = summary[0]['summary_text'].split(". ")
    return TaskPrioritizationResponse(prioritized_tasks=tasks)

# Endpoint for storing user feedback
@app.post("/feedback")
async def store_feedback(request: ProjectRequest):
    feedback_collection.insert_one({"project": request.project})
    return {"message": "Feedback stored successfully"}

# WebSocket for real-time chat
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Chat with the user: {data}",
            max_tokens=150
        )
        await websocket.send_text(response.choices[0].text.strip()) 