
---

# 🚀 DevIQ: AI-Powered Tech Stack & Task Optimizer 🤖

**DevIQ** is an AI-driven application designed to assist developers and project managers in optimizing their tech stack choices and task prioritization for IT projects. Leveraging the power of OpenAI's language models, DevIQ provides intelligent recommendations and prioritizations tailored to your project needs.

---

## ✨ Features

- **🔧 Tech Stack Recommendation**: Get AI-generated suggestions for the best technologies to use for your project, covering frontend, backend, databases, cloud services, and more.
- **📋 Task Prioritization**: Receive a structured list of prioritized tasks to streamline your project development process.
- **📝 User Feedback**: Collect and store user feedback to continuously improve the AI recommendations and prioritizations.

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
2. **Choose a feature**: Use the sidebar to select either "Tech Stack Recommendation" or "Task Prioritization".
3. **Enter project details**: Provide a detailed description of your project.
4. **Get results**: Click "🔍 Get Results" to receive AI-generated recommendations or prioritizations.
5. **Provide feedback**: Rate the results and provide additional feedback to help improve the AI's performance.

---

## 📂 File Structure

```
deviq/
├── backend/                  # Contains the Flask backend code
├── frontend/                 # Contains the Streamlit frontend code and styles
├── requirements.txt          # Lists the Python dependencies
├── .env                      # Stores environment variables (not included in the repository for security reasons)
└── README.md                 # Project documentation
```

---

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. **Fork the repository**.
2. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-nam
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
- **[OpenAI](https://openai.com/)** - AI language models
- **[LangChain](https://langchain.com/)** - AI integration

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

Made with ❤️ by **Birkity**.

---
