import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Streamlit App Configuration
st.set_page_config(page_title="DevIQ", page_icon="🤖", layout="centered")

# Custom CSS for themes and animations
with open("frontend/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to", ["Tech Stack Recommendation", "Task Prioritization"])

# App Title
st.title("🚀 DevIQ: AI-Powered Tech Stack & Task Optimizer")

# User Input Section
st.subheader("Describe Your Project:")
project_desc = st.text_area("Enter project details...", height=150)

if st.button("🔍 Get Results"):
    if project_desc.strip():
        with st.spinner("Processing..."):
            if option == "Tech Stack Recommendation":
                response = requests.post(f"{BACKEND_URL}/recommend", json={"project": project_desc})
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Recommendations Generated!")
                    
                    # Display Recommended Tech Stack
                    with st.expander("💡 Recommended Tech Stack:"):
                        for line in data["stack"]:
                            st.markdown(f"- {line}")

                    # User Feedback for Recommendations
                    st.subheader("Rate the Recommendations")
                    rating = st.slider("How would you rate these recommendations?", 1, 5, 3, key="recommendation_rating")
                    feedback = st.text_area("Additional feedback (optional):", height=100, key="recommendation_feedback")
                    
                    if st.button("Submit Feedback", key="submit_recommendation_feedback"):
                        feedback_response = requests.post(f"{BACKEND_URL}/feedback", json={
                            "project": project_desc,
                            "recommendation_or_prioritization": "\n".join(data["stack"]),
                            "rating": rating,
                            "feedback": feedback
                        })
                        if feedback_response.status_code == 200:
                            st.success("Thank you for your feedback!")
                        else:
                            st.error("Failed to submit feedback. Please try again.")
                else:
                    st.error("⚠️ Failed to fetch recommendations. Try again.")
            
            elif option == "Task Prioritization":
                response = requests.post(f"{BACKEND_URL}/prioritize_tasks", json={"project": project_desc})
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Task Prioritization Complete!")
                    
                    # Display Task Prioritization
                    with st.expander("📊 Task Prioritization:"):
                        for priority, task in enumerate(data["prioritized_tasks"], start=1):
                            st.markdown(f"**{priority}.** {task}")
                    
                    # User Feedback for Task Prioritization
                    st.subheader("Rate the Task Prioritization")
                    rating = st.slider("How would you rate this task prioritization?", 1, 5, 3)
                    feedback = st.text_area("Additional feedback (optional):", height=100)
                    
                    if st.button("Submit Feedback"):
                        feedback_response = requests.post(f"{BACKEND_URL}/feedback", json={
                            "project": project_desc,
                            "recommendation_or_prioritization": "\n".join(data["prioritized_tasks"]),
                            "rating": rating,
                            "feedback": feedback
                        })
                        if feedback_response.status_code == 200:
                            st.success("Thank you for your feedback!")
                        else:
                            st.error("Failed to submit feedback. Please try again.")
                else:
                    st.error("⚠️ Failed to fetch task prioritization. Try again.")
    else:
        st.warning("⚠️ Please enter project details.")

# Footer
st.markdown("---")
st.markdown("💻 Built with ❤️ using Streamlit & FastAPI")