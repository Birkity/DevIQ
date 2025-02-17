import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Streamlit App Configuration
st.set_page_config(page_title="DevIQ Task Prioritizer", page_icon="📊", layout="centered")

# Custom CSS for themes and animations
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Theme toggle
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])
st.markdown(f'<body class="{theme.lower()}">', unsafe_allow_html=True)

# App Title
st.title("📊 DevIQ: Task Prioritizer")

# User Input Section
st.subheader("Describe Your Project:")
project_desc = st.text_area("Enter project details...", height=150)

if st.button("🔍 Get Task Prioritization"):
    if project_desc.strip():
        with st.spinner("Analyzing tasks..."):
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
            else:
                st.error("⚠️ Failed to fetch task prioritization. Try again.")
    else:
        st.warning("⚠️ Please enter project details.")

# Footer
st.markdown("---")
st.markdown("💻 Built with ❤️ using Streamlit & FastAPI")

