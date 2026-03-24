# ✨ Ask DeX – Advanced Multimodal AI Assistant

Ask DeX is a **next-generation multimodal AI chatbot** built with **Streamlit** that can understand and process both **text and images** in real time. It delivers intelligent responses using a powerful vision-language model via the OpenRouter API.

This project demonstrates capabilities in **AI integration, real-time streaming, UI engineering, and multimodal interaction**.

---

## 🌟 Overview

Ask DeX is designed to act as an intelligent assistant capable of:

- Understanding user queries in natural language  
- Processing images (screenshots, documents, charts, etc.)  
- Providing real-time streamed responses  
- Supporting multiple use cases like OCR, debugging, and analysis  

---

## 🚀 Key Features

### 💬 Conversational AI
- Real-time chat interface with streaming responses  
- Maintains conversation history  
- Context-aware replies  

### 🖼️ Multimodal Input
- Accepts both **text and image inputs**
- Upload images directly from the UI  
- Displays image previews before sending  

### ⚡ Streaming Responses
- Uses **server-side streaming** for faster response rendering  
- Improves user experience with live typing effect  

### 🧠 AI Capabilities
- Image understanding (charts, UI, documents)  
- OCR (Extract text from images)  
- Code debugging from screenshots  
- Data insights and explanations  
- Creative suggestions  

### 🎨 Custom UI/UX
- Fully customized UI using HTML, CSS, and JavaScript inside Streamlit  
- Chat bubbles (user vs AI)  
- Typing animation  
- Interactive prompt cards  

### 🔐 Secure API Handling
- API key stored in environment file (`env`)  
- Loaded dynamically to avoid caching issues  

---

## 🛠️ Tech Stack

### 👨‍💻 Frontend
- Streamlit  
- Custom HTML, CSS, JavaScript  

### ⚙️ Backend
- Python  

### 🤖 AI Model
- OpenRouter API  
- Model: `qwen/qwen3-vl-235b-a22b-thinking` (Vision-Language Model)  

### 📦 Libraries
- streamlit >= 1.32.0  
- requests >= 2.31.0  
- python-dotenv >= 1.0.0  
- pillow >= 10.0.0  

---

## 📂 Project Structure

```
Ask-DeX/
│── app.py             # Main Streamlit app (UI + frontend logic)
│── model.py           # API integration and streaming logic
│── requirements.txt   # Python dependencies
│── env                # Environment variables (API key)
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git https://github.com/Madhanadeva-D/Ask-DeX-AI-ChatBot.git
cd ask-dex
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Create a file named `env` in the root directory:

```env
OPENROUTER_API_KEY=your_api_key_here
```

> ⚠️ Important: Never upload your `env` file to GitHub.

---

## ▶️ Running the Application

```bash
python -m streamlit run app.py
```

Open in browser:
```
http://localhost:8501
```

---

## 🧩 System Architecture

```
User Input (Text/Image)
        ↓
Streamlit UI (app.py)
        ↓
Message Formatting
        ↓
model.py (API Layer)
        ↓
OpenRouter API
        ↓
Streaming Response
        ↓
UI Rendering (Chat Interface)
```

---

## 🔄 How It Works (Detailed)

1. User enters text or uploads an image  
2. Image is converted to Base64 format  
3. Messages are structured for API compatibility  
4. Request is sent to OpenRouter API  
5. Streaming response is received chunk-by-chunk  
6. UI updates dynamically in real time  
7. Chat history is stored in session state  

---

## 📸 Supported Use Cases

- 🖹 Extract text from documents/images (OCR)  
- 🧑‍💻 Debug errors from screenshots  
- 📊 Analyze graphs and charts  
- 🎨 Generate creative ideas  
- 📱 Convert UI screenshots into code  
- 🤖 General-purpose AI assistant  

---

## 🎯 Example Prompts

- "Extract all text from this image"  
- "Find the bug in this code screenshot"  
- "Explain the trend in this chart"  
- "Improve this design idea"  

---

## ⚠️ Limitations

- Depends on external API availability  
- Response speed varies based on model load  
- Large images may increase processing time  

---

## 🔮 Future Improvements

- Add voice input/output  
- Chat history persistence (database)  
- Authentication system  
- Deployment on cloud (AWS / Render / Vercel)  
- Support for multiple AI models  

---

## ⭐ Support

If you like this project:

- ⭐ Star the repository  
- 🍴 Fork and improve it  
- 📢 Share with others  

---
