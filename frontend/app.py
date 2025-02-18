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

# Theme toggle
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])
st.markdown(f'<body class="{theme.lower()}">', unsafe_allow_html=True)

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
                        st.write(", ".join(data["stack"]))

                    # Display Latest Tech Trends
                    if "latest_trends" in data:
                        with st.expander("🔥 Latest Tech Trends:"):
                            st.write(data["latest_trends"])
                    
                    # User Feedback
                    st.subheader("Rate the Recommendations")
                    rating = st.slider("How would you rate these recommendations?", 1, 5, 3)
                    feedback = st.text_area("Additional feedback (optional):", height=100)
                    
                    if st.button("Submit Feedback"):
                        feedback_response = requests.post(f"{BACKEND_URL}/feedback", json={
                            "project": project_desc,
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
                        if "prioritized_tasks" in data:
                            for priority, task in enumerate(data["prioritized_tasks"], start=1):
                                st.write(f"{priority}. {task}")
                        else:
                            st.write("No prioritized tasks available.")
                    
                    # User Feedback
                    st.subheader("Rate the Task Prioritization")
                    rating = st.slider("How would you rate this task prioritization?", 1, 5, 3)
                    feedback = st.text_area("Additional feedback (optional):", height=100)
                    
                    if st.button("Submit Feedback"):
                        feedback_response = requests.post(f"{BACKEND_URL}/feedback", json={
                            "project": project_desc,
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

