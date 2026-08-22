<div align="center">

# 🤖 Sanskari AI Assistant

### An Intelligent Real-Time Voice AI Assistant built with Python, Google Gemini Live & LiveKit

<img src="assets\images/sanskari-gui.png" alt="Sanskari AI GUI" width="100%">

<br>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![LiveKit](https://img.shields.io/badge/LiveKit-Real--Time-blue?style=for-the-badge)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

### 🎙️ Talk Naturally • 🧠 Think Intelligently • ⚡ Respond Instantly

*A Modern Voice Assistant capable of understanding natural language, controlling your computer, searching the web, analyzing the screen, and interacting through a beautiful desktop interface.*

</div>

---

# 📖 About

Sanskari AI Assistant is a modern desktop Voice AI Assistant developed entirely in Python.

The assistant communicates with users in real time using voice, understands natural language, executes computer tasks, performs Google searches, analyzes the screen, controls applications, and responds naturally through Google Gemini Live.

Unlike traditional assistants, Sanskari AI focuses on providing a smooth conversational experience while integrating desktop automation, intelligent tools, and a modern graphical interface.

This project was designed to demonstrate how modern AI models can be combined with desktop automation to build an intelligent personal assistant.

---

# ✨ Features

## 🧠 AI Features

- Real-Time Voice Conversation
- Google Gemini Live Integration
- Natural Language Understanding
- Context-Aware Responses
- Multi-language Support
- Smart Prompt System
- Human-like Voice Interaction

---

## 🖥 Desktop Automation

- Open Applications
- Close Applications
- Open Websites
- Open Files
- Open Folders
- PDF Opening
- Keyboard Automation
- Mouse Automation
- Scroll Control
- Volume Control

---

## 🌍 Internet Features

- Google Search
- Current Date & Time
- Weather Information

---

## 👁 Vision Features

- Screen Analysis
- Code Error Detection
- Desktop Understanding

---

## 🎨 GUI Features

- Modern Dashboard
- Animated AI Ring
- Live Status Updates
- Chat Panel
- Beautiful Interface
- Real-Time Event Display

---

## ⚙ Technical Features

- Async Programming
- LiveKit Integration
- IPC Communication
- Modular Architecture
- Plugin Based Design
- Clean Code Structure
- Easy Scalability

---

# 🖥 GUI Preview

<div align="center">

## Sanskari AI Desktop Interface

<img src="assets\images/sanskari-gui.png" width="100%">

</div>

The graphical interface provides:

- Beautiful AI Ring
- Live Conversation
- Status Monitoring
- Voice State
- Assistant Activity
- Tool Execution Status
- Modern Dashboard Experience

---

# 📂 Project Structure

```text
Sanskari-AI/
│
├── agent.py                     # Main AI Agent
├── run.py                       # Project Entry Point
├── requirements.txt             # Python Dependencies
├── README.md                    # Documentation
├── .env.example                 # Environment Variables Example
│
├── assets/
│   └── gui-preview.png          # GUI Screenshot
│
├── main/
│   ├── core/
│   │   ├── ipc/
│   │   ├── events/
│   │   └── controller/
│   │
│   ├── memory/
│   │
│   ├── gui/
│   │
│   ├── tools/
│   │
│   ├── vision/
│   │
│   ├── prompts/
│   │
│   └── ...
│
└── ...
```

---

# 🏗 Project Architecture

```text
                    User Voice
                        │
                        ▼
              Speech Recognition
                        │
                        ▼
               Google Gemini Live
                        │
                        ▼
              Intelligent AI Agent
                        │
      ┌─────────────────┼─────────────────┐
      │                 │                 │
      ▼                 ▼                 ▼
 Google Search     Desktop Tools     Vision Tools
      │                 │                 │
      └─────────────────┼─────────────────┘
                        │
                        ▼
                  GUI Interface
                        │
                        ▼
                 Voice Response
```

---

# ⚙ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core Programming Language |
| Google Gemini Live | AI Brain |
| LiveKit | Real-Time Voice Communication |
| PyQt6 | Desktop GUI |
| Asyncio | Asynchronous Programming |
| SQLite | Local Storage |
| Dotenv | Environment Variables |
| IPC | Communication Between Components |
| Windows API | Desktop Automation |

---

# 📦 Dependencies

Major libraries used in this project:

- livekit
- livekit-agents
- google-generativeai
- PyQt6
- PyQt6-WebEngine
- python-dotenv
- pillow
- mss
- requests
- sqlite3
- asyncio

---

# 🚀 Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YourUsername/Sanskari-AI.git
```

```bash
cd Sanskari-AI
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment

Create a file named

```text
.env
```

Add your API Keys

```env
GOOGLE_API_KEY=YOUR_API_KEY
LIVEKIT_URL=YOUR_URL
LIVEKIT_API_KEY=YOUR_KEY
LIVEKIT_API_SECRET=YOUR_SECRET
```

---

# ▶ Running the Project

Start the assistant

```bash
python run.py
```

or

```bash
python agent.py
```

(depending on your project structure)

---

# 💻 Supported Platform

✔ Windows 10

✔ Windows 11

Linux support is planned in future versions.

---

# 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| GOOGLE_API_KEY | Google Gemini API |
| LIVEKIT_URL | LiveKit Server URL |
| LIVEKIT_API_KEY | LiveKit API Key |
| LIVEKIT_API_SECRET | LiveKit Secret |

---

# 📌 Requirements

- Python 3.11+
- Internet Connection
- Google Gemini API
- LiveKit Configuration
- Windows Operating System
- Microphone
- Speakers

---

# 🎙 Voice Commands

Sanskari AI understands natural language commands.

## 🌐 Internet

```text
Search Python tutorials

Search latest AI news

What is Machine Learning?

Search OpenAI
```

---

## 🌦 Weather

```text
What's the weather today?

Delhi weather

Will it rain tomorrow?

Current temperature
```

---

## 🕒 Date & Time

```text
Current time

Today's date

What day is today?
```

---

## 💻 Application Control

```text
Open Chrome

Open VS Code

Close Chrome

Open Calculator

Open Downloads folder
```

---

## 📁 File Operations

```text
Open my PDF

Play music

Open Desktop

Open Documents
```

---

## 🖱 Mouse Control

```text
Move cursor left

Move cursor right

Scroll down

Scroll up

Mouse click
```

---

## ⌨ Keyboard Control

```text
Type Hello World

Press Enter

Press Ctrl + S

Press Ctrl + Shift + P

Press Backspace
```

---

## 🔊 System Control

```text
Increase Volume

Decrease Volume

Mute Volume
```

---

## 👁 Screen Analysis

```text
Analyze my screen

What is on my screen?

Check coding error

Read screen
```

---

# 🧰 Available Tools

| Tool | Description |
|------|-------------|
| Google Search | Search information from the Internet |
| Weather | Live weather information |
| Date & Time | Current date and time |
| Vision | Analyze desktop screen |
| Window Control | Open & Close applications |
| File Manager | Open files and folders |
| Keyboard Control | Keyboard automation |
| Mouse Control | Cursor automation |
| Volume Control | System volume management |

---

# 🧠 AI Capabilities

✔ Natural Conversation

✔ Real-Time Voice Processing

✔ Intelligent Responses

✔ Desktop Automation

✔ Screen Understanding

✔ Internet Search

✔ Weather Information

✔ Context Awareness

✔ Human-like Voice Interaction

✔ Modular Architecture

✔ Tool Calling

✔ Multi-language Support

---

# 📸 Project Screenshots

## 🏠 Main Dashboard

<img src="assets/gui-preview.png" width="100%">

---

## 🎤 Voice Interaction

The assistant listens to your voice in real time and responds naturally.

---

## ⚡ Desktop Automation

Control your computer completely using voice commands.

---

## 👁 Screen Vision

Analyze the desktop and help solve coding or application problems instantly.

---

# 🚀 Roadmap

Future improvements planned for Sanskari AI.

- [ ] Persistent Memory System
- [ ] Long-Term Conversation Memory
- [ ] Offline Mode
- [ ] Plugin System
- [ ] Linux Support
- [ ] macOS Support
- [ ] OCR Text Reading
- [ ] Face Recognition
- [ ] Wake Word Detection
- [ ] Smart Task Automation
- [ ] Mobile Companion App
- [ ] Calendar Integration
- [ ] Email Automation
- [ ] Multi-Agent Collaboration

---

# 🤝 Contributing

Contributions are always welcome.

If you'd like to improve Sanskari AI:

1. Fork this repository
2. Create a new feature branch
3. Commit your changes
4. Push your branch
5. Open a Pull Request

Every contribution is appreciated ❤️

---

# 🛡 License

This project is licensed under the **MIT License**.

You are free to use, modify and distribute this project while keeping the original license.

---

# 👨‍💻 Developer

## Anmol Singh

**BCA Student | Python Developer | AI Enthusiast | Future Software Engineer**

Passionate about building intelligent desktop applications, AI assistants and automation tools using Python.

Current interests:

- Artificial Intelligence
- Desktop Automation
- Computer Vision
- Software Engineering
- Human Computer Interaction

---

# 💙 Acknowledgements

Special thanks to:

- Google Gemini
- LiveKit
- Python Community
- Open Source Community
- PyQt Developers

Without these amazing technologies this project wouldn't have been possible.

---

# 📬 Contact

GitHub

> https://github.com/Anmolkumar108

LinkedIn

> *(Add your LinkedIn URL here)*

Email

> *(Add your Email here)*

---

# ⭐ Support the Project

If you like this project,

⭐ Star this repository

🍴 Fork it

📢 Share it with others

Your support motivates future development.

---

# 📊 Project Status

**Current Version**

```text
v3.0
```

**Status**

```text
🟢 Active Development
```

---

# ❤️ Final Words

Sanskari AI is more than just a voice assistant.

It represents months of learning, experimenting, debugging, and improving.

Every feature, every bug fix, and every line of code has been a valuable part of the learning journey.

Thank you for visiting this project.

Happy Coding! 🚀

---

<p align="center">

Made with ❤️ using Python

by

<b>Anmol Singh</b>

</p>