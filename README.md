# Readora AI

Readora AI is an accessibility-first reading assistant built for dyslexic, ADHD, and neurodivergent learners. It transforms dense academic text and scanned PDFs into clean, digestible prose using custom typography, parallel AI text simplification, and synchronized word-by-word text-to-speech narration.

Developed for the **IncludEDU Neurodiversity Hackathon 2026**.

---

## ✨ Key Features

* **⚡ Parallel Multi-Key Processing:** Utilizes a custom multi-account Groq API key pooling and rotation system to process large documents and scanned pages simultaneously without hitting rate limits.
* **📄 Smart PDF & Vision OCR:** Instantly extracts text from native digital PDFs or runs asynchronous Vision OCR on scanned/photo-based PDFs using PyMuPDF (`fitz`).
* **🤖 AI Text Simplification:** Breaks down complex, jargon-heavy paragraphs into clear, literal sentences tailored for different reading levels, alongside an auto-generated vocabulary list.
* **🔊 Synchronized Text-to-Speech:** Features an interactive audio reader with real-time word-by-word highlighting and a keep-alive engine to ensure smooth, uninterrupted playback.
* **🎨 Custom Accessibility Layout:** Styled with the *OpenDyslexic* typeface, adjustable line-spacing controls, custom font-sizing sliders, and a low-sensory paper reading pane.
* **📚 Persistent Workspace:** Secure local authentication with persistent document history and profile picture management backed by SQLite.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit, HTML5, CSS3, JavaScript, Custom UI Components
* **Backend:** Python, FastAPI, Uvicorn, Asynchronous Concurrency (`asyncio`)
* **AI & OCR:** Groq API (`llama-3.1-8b-instant`, Vision models), PyMuPDF (`fitz`)
* **Database:** SQLite (`users.db`)

---

## 📂 Project Structure

\`\`\`text
Readora-AI/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   └── services/
│   ├── main.py
│   └── database.py
├── FrontEnd/
│   ├── components/
│   ├── assets/
│   ├── app.py
│   ├── styles.py
│   └── utils.py
├── run.py
└── requirements.txt
\`\`\`

---

## 🚀 Getting Started

**1. Clone the repository:**

\`\`\`bash
git clone https://github.com/mayank-nova/Readora-AI.git
cd Readora-AI
\`\`\`

**2. Install dependencies:**

\`\`\`bash
pip install -r requirements.txt
\`\`\`

**3. Configure your API keys:**

Create a `.env` file inside the `backend/` directory and add your Groq API keys:

\`\`\`
GROQ_API_KEY_1=gsk_...
GROQ_API_KEY_2=gsk_...
\`\`\`

**4. Run the application:**

\`\`\`bash
python run.py
\`\`\`

This will automatically launch both the FastAPI backend server and the Streamlit frontend.

---

## 👥 Team

Created by the engineering team from NSUT for the IncludEDU Neurodiversity Hackathon 2026.

## 📄 License

This project is intended for educational and hackathon purposes.
