import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Streamlit App Configuration
st.set_page_config(page_title="DevIQ", page_icon="🤖", layout="wide")

# Custom CSS for themes and animations
with open("frontend/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Theme toggle
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])
st.markdown(f'<body class="{theme.lower()}">', unsafe_allow_html=True)

# App Title
st.title("🚀 DevIQ: AI-Powered Tech Stack & Task Optimizer")

# User Input Section
st.subheader("Describe Your Project:")
project_desc = st.text_area("Enter project details...", height=100)

if st.button("🔍 Get Recommendations"):
    if project_desc.strip():
        with st.spinner("Generating recommendations..."):
            response = requests.post(f"{BACKEND_URL}/recommend", json={"project": project_desc})
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Recommendations Generated!")
                
                # Display Recommended Tech Stack
                with st.expander("💡 Recommended Tech Stack:"):
                    st.write(", ".join(data["stack"]))

                # Display Task Breakdown
                with st.expander("📌 Task Breakdown:"):
                    for task in data["tasks"]:
                        st.write(f"- {task}")

                # Display Latest Tech Trends
                if "latest_trends" in data:
                    with st.expander("🔥 Latest Tech Trends:"):
                        st.write(data["latest_trends"])

            else:
                st.error("⚠️ Failed to fetch recommendations. Try again.")
    else:
        st.warning("⚠️ Please enter project details.")

# Feedback Section
st.subheader("💬 Provide Feedback:")
feedback_text = st.text_area("Enter your feedback...")

if st.button("📨 Submit Feedback"):
    if feedback_text.strip():
        feedback_response = requests.post(f"{BACKEND_URL}/feedback", json={"project": project_desc, "feedback": feedback_text})
        if feedback_response.status_code == 200:
            st.success("✅ Feedback submitted successfully!")
        else:
            st.error("⚠️ Failed to submit feedback.")
    else:
        st.warning("⚠️ Please enter feedback.")

# Footer
st.markdown("---")
st.markdown("💻 Built with ❤️ using Streamlit & FastAPI")

