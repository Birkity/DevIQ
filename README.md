

# 🚀 DevIQ: AI-Powered Tech Stack & Task Optimizer 🤖

**DevIQ** is an AI-driven application that helps developers and project managers **optimize their tech stack choices** and **prioritize tasks** efficiently. By leveraging OpenAI’s **language models**, GitHub repository data, and user feedback, **DevIQ continuously improves its recommendations** to align with the latest industry trends.

---

## ✨ Features

- **🔧 AI-Powered Tech Stack Recommendation**  
  - Get **optimized** technology recommendations based on project needs.  
  - Covers **Frontend, Backend, Databases, Cloud, DevOps, and APIs**.  
  - Uses **GitHub repository data** to suggest trending technologies.  

- **📋 Intelligent Task Prioritization**  
  - Break down **projects into structured, step-by-step tasks**.  
  - Prioritizes tasks based on **dependencies, deadlines, and impact**.  

- **📝 Adaptive AI Feedback System**  
  - Collects **user ratings and feedback** to refine AI-generated recommendations.  
  - Dynamically adjusts **prompt structures** to improve accuracy.  

---

## 🛠️ Installation

### Prerequisites

- **Python 3.7 or higher**
- **[pip](https://pip.pypa.io/en/stable/installation/)**
- **[Node.js](https://nodejs.org/)** (for frontend development)

---

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/deviq.git
   cd deviq
   ```

2. **Install backend dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the root directory and add your API keys:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key
     GITHUB_API_TOKEN=your_github_api_token
     OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
     BACKEND_URL=http://127.0.0.1:8000
     ```

4. **Run the backend server**:
   ```bash
   python backend/main.py
   ```

5. **Run the frontend application**:
   ```bash
   streamlit run frontend/app.py
   ```

---

## 🎯 Usage

1. **Navigate to the application**: Open your web browser and go to `http://localhost:8501`.
2. **Choose a feature**:  
   - **"Tech Stack Recommendation"** for AI-driven technology choices.  
   - **"Task Prioritization"** for structured task management.  
3. **Enter project details**: Provide a detailed project description.
4. **Get AI-powered results**: Click **"🔍 Get Results"** to receive tailored recommendations.
5. **Review GitHub insights**: Get **top trending GitHub repositories** related to your project.
6. **Provide feedback**: Rate the results to improve future recommendations.

---

## 📂 File Structure

```
deviq/
├── backend/                  # Flask backend for AI processing
│   ├── main.py               # Main backend server file
│   ├── analyze_feedback.py   # Feedback processing and prompt adjustment
│   ├── requirements.txt      # Python dependencies
├── frontend/                 # Streamlit-based frontend
│   ├── app.py                # Main Streamlit application
│   ├── styles.css            # Custom UI styles
├── .env                      # Environment variables (not included in repo)
├── README.md                 # Project documentation
└── LICENSE                   # License file
```

---

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. **Fork the repository**.
2. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes**:
   ```bash
   git commit -m "Add your message here"
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Submit a pull request**.

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 💻 Built With

- **[Streamlit](https://streamlit.io/)** - Frontend framework
- **[Flask](https://flask.palletsprojects.com/)** - Backend framework
- **[LangChain](https://langchain.com/)** - AI pipeline management
- **[GitHub API](https://docs.github.com/en/rest)** - Fetch trending repositories
- **[OpenAI](https://openai.com/)** - AI-powered recommendations

---

## 🙏 Acknowledgments

- Thanks to **OpenAI** for providing the powerful language models.
- Thanks to the **Streamlit** and **Flask** communities for their amazing tools.

---

## 📞 Contact

For any questions or feedback, feel free to reach out:

- **Email**: lily.yishak2@gmail.com
- **GitHub**: [Birkity](https://github.com/Birkity)

---

**Made with ❤️ by Birkity.**

Let me know if you need any changes! 🚀
