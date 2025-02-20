from flask import Flask, request, jsonify
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import os
import csv
import subprocess
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")

if not OPENAI_API_KEY or not OPENROUTER_BASE_URL:
    raise ValueError("Missing API keys! Ensure OPENAI_API_KEY and OPENROUTER_BASE_URL are set.")

# Initialize Flask app
app = Flask(__name__)

# Initialize LangChain with OpenRouter
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    openai_api_base=OPENROUTER_BASE_URL,
    model_name="gpt-3.5-turbo",
)

# File paths
ANALYSIS_FILE = "feedback_analysis.json"
FEEDBACK_FILE = "feedback.csv"

# Load Feedback Analysis
def load_feedback_analysis():
    if os.path.exists(ANALYSIS_FILE):
        with open(ANALYSIS_FILE, "r") as f:
            return json.load(f)
    return {"average_rating": 0, "common_feedback": []}

feedback_analysis = load_feedback_analysis()
average_rating = feedback_analysis.get("average_rating", 0)
common_feedback = feedback_analysis.get("common_feedback", [])

# Extract only feedback text to adjust prompts
common_feedback_texts = [fb[0] if isinstance(fb, (list, tuple)) and len(fb) > 0 else str(fb) for fb in common_feedback]

# Dynamically adjust the prompt template based on feedback trends
if "too generic" in common_feedback_texts:
    prompt_adjustment = "Provide more project-specific recommendations."
elif "too complex" in common_feedback_texts:
    prompt_adjustment = "Use simpler explanations and beginner-friendly options."
else:
    prompt_adjustment = ""

# Function to fetch GitHub repository data to enhance recommendations
def fetch_github_repos(topic):
    url = f"https://api.github.com/search/repositories?q={topic}&sort=stars&order=desc"
    headers = {"Authorization": f"token {GITHUB_API_TOKEN}"} if GITHUB_API_TOKEN else {}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos = response.json().get("items", [])[:5]
        return [{"name": repo["name"], "url": repo["html_url"], "description": repo["description"]} for repo in repos]
    return []

# Define a prompt template for tech stack recommendation
tech_stack_prompt_template = PromptTemplate(
    input_variables=["project"],
    template=f"""
    🌟 **AI-Powered Tech Stack Recommendation** 🌟

    You are an AI assistant specializing in **technology stack recommendations** for the IT industry, including **web, mobile, backend, APIs, cloud, and DevOps**.  
    {prompt_adjustment}

    🔍 **Project Description:** {{project}}  

    Provide a **detailed, structured** recommendation considering scalability, security, performance, and ease of integration.

    ### **Recommended Tech Stack**
    - **Frontend Technologies (UI/UX):** 🎨  
    - **Backend Technologies (Business Logic & APIs):** 🛠️  
    - **Database Solutions (Storage & Performance):** 🗄️  
    - **Cloud & DevOps (Scalability & Deployment):** ☁️  
    - **User Authentication & Security:** 🔐  
    - **File Storage & CDN (Media & Static Content):** 📂  
    - **Third-Party Integrations & APIs:** 🔗  

    ✅ **Ensure recommendations align with industry best practices and emerging trends.**
    """
)

# Define a prompt template for task prioritization
task_prioritization_prompt_template = PromptTemplate(
    input_variables=["project"],
    template=f"""
    📋 **AI-Powered Task Prioritization for Project Execution** 📋

    You are an AI assistant specializing in **task management and workflow optimization** for IT projects.  
    {prompt_adjustment}

    🔍 **Project Description:** {{project}}  

    Provide a **structured, step-by-step** task prioritization plan.

    ### **Optimized Task Execution Plan**  
    **1️⃣ Initial Setup & Planning** ⚙️  
    **2️⃣ Core Feature Development** 🚀  
    **3️⃣ User Interface & Experience** 🎨  
    **4️⃣ Testing & Quality Assurance** ✅  
    **5️⃣ Deployment & Optimization** 🚀  
    **6️⃣ Post-Launch & Maintenance** 🔄  

    ✅ **Ensure tasks are logically ordered with clear dependencies.**  
    """
)

# Initialize memory for conversation context
memory = ConversationBufferMemory(
    memory_key="history",
    input_key="project",
    max_token_limit=2000
)

# Custom LLM Chain
class CustomLLMChain(LLMChain):
    def __init__(self, llm, memory, prompt):
        super().__init__(llm=llm, memory=memory, prompt=prompt)

    def run(self, input_data):
        formatted_input = {
            "project": input_data.get("project", ""),
            "history": self.memory.buffer,
        }
        response = self.predict(**formatted_input)
        self.memory.save_context({"project": input_data.get("project", "")}, {"output": response})
        return response

# Create chains
tech_stack_chain = CustomLLMChain(llm=llm, memory=memory, prompt=tech_stack_prompt_template)
task_prioritization_chain = CustomLLMChain(llm=llm, memory=memory, prompt=task_prioritization_prompt_template)

# Function to write data to a CSV file
def write_to_csv(file_path, data):
    file_exists = os.path.exists(file_path)
    
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Project", "Output"])
        writer.writerow(data)

# Endpoint for tech stack recommendation
@app.route('/recommend', methods=['POST'])
def recommend_tech_stack():
    data = request.json
    project_desc = data.get('project', '')

    if not project_desc:
        return jsonify({"error": "Project description is required"}), 400

    try:
        response = tech_stack_chain.run({"project": project_desc})
        github_repos = fetch_github_repos(project_desc)
        write_to_csv('recommendations.csv', [project_desc, response])

        return jsonify({"stack": response, "github_repos": github_repos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint for task prioritization
@app.route('/prioritize_tasks', methods=['POST'])
def prioritize_tasks():
    data = request.json
    project_desc = data.get('project', '')

    if not project_desc:
        return jsonify({"error": "Project description is required"}), 400

    try:
        response = task_prioritization_chain.run({"project": project_desc})
        write_to_csv('task_prioritizations.csv', [project_desc, response])

        return jsonify({"prioritized_tasks": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint for analyzing feedback
@app.route('/analyze_feedback', methods=['POST'])
def analyze_and_update():
    subprocess.run(["python", "analyze_feedback.py"])
    
    with open(ANALYSIS_FILE, 'r') as f:
        analysis_results = json.load(f)

    return jsonify({"analysis": analysis_results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
