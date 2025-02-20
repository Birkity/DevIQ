import streamlit as st
import requests
import json

# Backend API URL
BACKEND_URL = "http://127.0.0.1:8000"

# Streamlit UI
st.set_page_config(page_title="DevIQ - AI Tech Stack & Task Optimizer", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .reportview-container {
        background: #f8f9fa;
    }
    .big-font {
        font-size:18px !important;
    }
    .stButton>button {
        font-size: 16px !important;
        background-color: #4CAF50;
        color: white;
        width: 100%;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Title & Description
st.title("🚀 DevIQ - AI Tech Stack & Task Optimizer")
st.write("Leverage AI to **recommend the best tech stacks** and **prioritize tasks** for your projects!")

# Sidebar Navigation
page = st.sidebar.radio("Navigate", ["Tech Stack Recommendation", "Task Prioritization", "Feedback & Analysis"])

# 🚀 Tech Stack Recommendation Page
if page == "Tech Stack Recommendation":
    st.header("🔍 Get AI-Powered Tech Stack Recommendations")
    
    # Input for project description
    project_desc = st.text_area("Describe your project", placeholder="E.g., A mobile e-commerce app with secure payments...")
    
    if st.button("Generate Recommendation"):
        if project_desc:
            with st.spinner("🔄 AI is analyzing your project..."):
                response = requests.post(f"{BACKEND_URL}/recommend", json={"project": project_desc})
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Tech Stack Recommendation Generated!")
                    st.write("\n".join(result["stack"]))
                else:
                    st.error("⚠️ Error: Unable to fetch recommendations.")
        else:
            st.warning("⚠️ Please provide a project description.")

# 📋 Task Prioritization Page
elif page == "Task Prioritization":
    st.header("📌 Get AI-Powered Task Prioritization")
    
    # Input for project description
    project_desc = st.text_area("Describe your project", placeholder="E.g., A SaaS platform for data visualization...")
    
    if st.button("Generate Task Plan"):
        if project_desc:
            with st.spinner("🔄 AI is prioritizing tasks..."):
                response = requests.post(f"{BACKEND_URL}/prioritize_tasks", json={"project": project_desc})
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Task Prioritization Plan Generated!")
                    st.write("\n".join(result["prioritized_tasks"]))
                else:
                    st.error("⚠️ Error: Unable to fetch task prioritization.")
        else:
            st.warning("⚠️ Please provide a project description.")

# 📝 Feedback Submission & Analysis Page
elif page == "Feedback & Analysis":
    st.header("📝 Submit Feedback & View Analysis")
    
    # Input fields for feedback
    project_desc = st.text_area("Describe the project for feedback", placeholder="E.g., AI chatbot for mental health support...")
    rating = st.slider("Rate the AI recommendation (1 - Poor, 5 - Excellent)", 1, 5, 3)
    feedback = st.text_area("Provide additional feedback", placeholder="E.g., The recommendations were too generic...")
    feedback_type = st.selectbox("Feedback Type", ["Tech Stack Recommendation", "Task Prioritization"])
    
    if st.button("Submit Feedback"):
        if project_desc and feedback:
            with st.spinner("🔄 Submitting feedback..."):
                data = {
                    "project": project_desc,
                    "rating": rating,
                    "feedback": feedback,
                    "recommendation_or_prioritization": feedback_type
                }
                response = requests.post(f"{BACKEND_URL}/feedback", json=data)
                if response.status_code == 200:
                    st.success("✅ Feedback submitted successfully!")
                else:
                    st.error("⚠️ Error submitting feedback.")
        else:
            st.warning("⚠️ Please fill out all fields.")

    # 📊 View Feedback Analysis
    if st.button("Analyze Feedback Trends"):
        with st.spinner("🔄 Analyzing feedback..."):
            response = requests.post(f"{BACKEND_URL}/analyze_feedback")
            if response.status_code == 200:
                analysis = response.json()
                st.success("✅ Feedback Analysis Completed!")
                st.write(f"**Average Rating:** {analysis['analysis']['average_rating']}")
                # Ensure the data is correctly structured
                common_feedback = analysis.get('analysis', {}).get('common_feedback', [])

                common_feedback_texts = [fb[0] if isinstance(fb, (list, tuple)) and len(fb) > 0 else str(fb) for fb in common_feedback]

                st.write(f"**Common Feedback Trends:** {', '.join(common_feedback_texts) if common_feedback_texts else 'No feedback trends available.'}")

            else:
                st.error("⚠️ Error fetching feedback analysis.")

