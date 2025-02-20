from flask import Flask, request, jsonify
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import os
import csv
import subprocess
import json
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

# Load Feedback Analysis
ANALYSIS_FILE = "feedback_analysis.json"

def load_feedback_analysis():
    if os.path.exists(ANALYSIS_FILE):
        with open(ANALYSIS_FILE, "r") as f:
            return json.load(f)
    return {"average_rating": 0, "common_feedback": []}

feedback_analysis = load_feedback_analysis()
average_rating = feedback_analysis["average_rating"]
common_feedback = [fb[0] for fb in feedback_analysis["common_feedback"]]

# Dynamically adjust the prompt template based on feedback trends
if "too generic" in common_feedback:
    prompt_adjustment = "Provide more project-specific recommendations."
elif "too complex" in common_feedback:
    prompt_adjustment = "Use simpler explanations and beginner-friendly options."
else:
    prompt_adjustment = ""

# Define a prompt template for tech stack recommendation
tech_stack_prompt_template = PromptTemplate(
    input_variables=["project"],
    template="""
    🌟 **AI-Powered Tech Stack Recommendation** 🌟

    You are an AI assistant specializing in **technology stack recommendations** for the IT industry, including **web, mobile, backend, APIs, cloud, and DevOps**.  

    🔍 **Project Description:** {project}  

    Provide a **detailed, structured** recommendation considering scalability, security, performance, and ease of integration. Your response should **clearly justify** each choice.  

    ### **Recommended Tech Stack**
    - **Frontend Technologies (UI/UX):** 🎨  
      _(Best frameworks/libraries for a responsive and dynamic UI, including state management and styling options.)_  

    - **Backend Technologies (Business Logic & APIs):** 🛠️  
      _(Programming languages, frameworks, and architectures like monolithic/microservices.)_  

    - **Database Solutions (Storage & Performance):** 🗄️  
      _(SQL vs NoSQL, indexing strategies, and real-time data needs.)_  

    - **Cloud & DevOps (Scalability & Deployment):** ☁️  
      _(Hosting platforms, CI/CD pipelines, and containerization tools.)_  

    - **User Authentication & Security:** 🔐  
      _(OAuth, JWT, Multi-Factor Authentication, encryption techniques.)_  

    - **File Storage & CDN (Media & Static Content):** 📂  
      _(Best storage solutions for performance, cost, and reliability.)_  

    - **Third-Party Integrations & APIs:** 🔗  
      _(CRM, payment gateways, analytics, and external services.)_  

    ✅ **Ensure recommendations align with industry best practices, emerging trends, and project-specific needs.** Provide **alternative options** where relevant.  
    """
)


# Define a prompt template for task prioritization
task_prioritization_prompt_template = PromptTemplate(
    input_variables=["project"],
    template="""
    📋 **AI-Powered Task Prioritization for Project Execution** 📋

    You are an AI assistant specializing in **task management and workflow optimization** for IT projects, including **web, mobile, backend, APIs, and cloud solutions**.  

    🔍 **Project Description:** {project}  

    Provide a **structured, step-by-step** task prioritization plan, considering dependencies, team workload, and deadlines.  

    ### **Optimized Task Execution Plan**  
    **1️⃣ Initial Setup & Planning** ⚙️  
       - _(Project requirements, tech stack decisions, repository setup, cloud configurations.)_  

    **2️⃣ Core Feature Development** 🚀  
       - _(Backend APIs, database schema design, authentication, main business logic.)_  

    **3️⃣ User Interface & Experience** 🎨  
       - _(Frontend development, component architecture, responsiveness, accessibility.)_  

    **4️⃣ Testing & Quality Assurance** ✅  
       - _(Unit testing, integration testing, security testing, bug fixes.)_  

    **5️⃣ Deployment & Optimization** 🚀  
       - _(CI/CD setup, cloud deployment, scalability tests, load balancing.)_  

    **6️⃣ Post-Launch & Maintenance** 🔄  
       - _(Monitoring, user feedback integration, security patches, performance updates.)_  

    ✅ **Ensure tasks are logically ordered with clear dependencies. Provide additional sub-tasks if necessary for complex implementations.**  
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
            "history": self.memory.buffer,  # Include conversation history
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
            writer.writerow(["Project", "Output"])  # Write header if file does not exist
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
        recommended_stack = response.strip().split("\n")
        write_to_csv('recommendations.csv', [project_desc, *recommended_stack])

        return jsonify({"stack": recommended_stack})
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
        prioritized_tasks = response.strip().split("\n")
        write_to_csv('task_prioritizations.csv', [project_desc, *prioritized_tasks])

        return jsonify({"prioritized_tasks": prioritized_tasks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint for storing user feedback
@app.route('/feedback', methods=['POST'])
def store_feedback():
    data = request.json
    project_desc = data.get('project', '')
    rating = data.get('rating', '')
    feedback = data.get('feedback', '')
    recommendation_or_prioritization = data.get('recommendation_or_prioritization', '')

    feedback_data = [project_desc, recommendation_or_prioritization, rating, feedback]
    write_to_csv('feedback.csv', feedback_data)

    return jsonify({"message": "Feedback stored successfully"}), 200

# Function to analyze feedback and update prompt
@app.route('/analyze_feedback', methods=['POST'])
def analyze_and_update():
    subprocess.run(["python", "analyze_feedback.py"])
    
    with open(ANALYSIS_FILE, 'r') as f:
        analysis_results = json.load(f)

    return jsonify({"analysis": analysis_results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)