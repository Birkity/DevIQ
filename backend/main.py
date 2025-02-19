from flask import Flask, request, jsonify
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
import csv

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

# Define a prompt template for tech stack recommendation
tech_stack_prompt_template = PromptTemplate(
    input_variables=["project"],
    template="""
    🌟 **AI Assistant for Tech Stack Recommendation** 🌟

    You are an AI assistant tasked with recommending a tech stack for IT industry including web, mobile, backend, APIs, cloud etc. 
    The project description is as follows: {project}.

    Please consider the following aspects and provide a detailed and structured recommendation for each, using bullet points for clarity:

    - **Frontend Technologies**: 🎨
    - **Backend Technologies**: 🛠️
    - **Database Solutions**: 🗄️
    - **Cloud Services**: ☁️
    - **User Authentication**: 🔐
    - **File Storage Solutions**: 📂
    - **Social Media Integration**: 📱

    Ensure that your recommendations are up-to-date with current industry standards and trends.
    """
)

# Define a prompt template for task prioritization
task_prioritization_prompt_template = PromptTemplate(
    input_variables=["project"],
    template="""
    📋 **AI Assistant for Task Prioritization** 📋

    You are an AI assistant tasked with prioritizing tasks for any application project in IT industry including web, mobile, backend, APIs, cloud etc. 
    The project description is as follows: {project}.

    Please consider the following aspects and provide a detailed and structured task prioritization list, using bullet points for clarity:

    1. **Initial Setup and Configuration**: ⚙️
    2. **Core Feature Development**: 🚀
    3. **User Interface Design**: 🎨
    4. **Testing and Quality Assurance**: ✅
    5. **Deployment and Maintenance**: 🛠️

    Make sure the tasks are ordered by priority and include any necessary sub-tasks for clarity.
    """
)

# Initialize memory for conversation context
memory = ConversationBufferMemory(
    memory_key="history",
    input_key="project",
    max_token_limit=2000  
)

# Create a custom chain class
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

# Create custom chains for tech stack recommendation and task prioritization
tech_stack_chain = CustomLLMChain(
    llm=llm,
    memory=memory,
    prompt=tech_stack_prompt_template
)

task_prioritization_chain = CustomLLMChain(
    llm=llm,
    memory=memory,
    prompt=task_prioritization_prompt_template
)

# Function to write data to a CSV file
def write_to_csv(file_path, data):
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Endpoint for tech stack recommendation
@app.route('/recommend', methods=['POST'])
def recommend_tech_stack():
    data = request.json
    project_desc = data.get('project', '')

    if not project_desc:
        return jsonify({"error": "Project description is required"}), 400

    try:
        # Use the custom chain to generate recommendations
        response = tech_stack_chain.run({"project": project_desc})
        recommended_stack = response.strip().split("\n")

        if not recommended_stack or recommended_stack == [""]:
            return jsonify({"error": "No recommendations found"}), 404

        # Store recommendation in CSV
        write_to_csv('recommendations.csv', [project_desc, *recommended_stack])

        return jsonify({"stack": recommended_stack})
    except Exception as e:
        # Log the exception and return an error response
        print(f"Error generating recommendations: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Endpoint for task prioritization
@app.route('/prioritize_tasks', methods=['POST'])
def prioritize_tasks():
    data = request.json
    project_desc = data.get('project', '')

    if not project_desc:
        return jsonify({"error": "Project description is required"}), 400

    # Use the custom chain to generate task prioritization
    response = task_prioritization_chain.run({"project": project_desc})
    prioritized_tasks = response.strip().split("\n")

    if not prioritized_tasks or prioritized_tasks == [""]:
        return jsonify({"error": "No tasks prioritized"}), 404

    # Store task prioritization in CSV
    write_to_csv('task_prioritizations.csv', [project_desc, *prioritized_tasks])

    return jsonify({"prioritized_tasks": prioritized_tasks})

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

    return jsonify({"message": "Feedback stored successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)