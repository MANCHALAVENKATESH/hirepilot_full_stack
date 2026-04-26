# AI Technical Assessment Platform

An interactive AI-powered technical assessment platform with:

- Voice-first candidate interview flow
- AI avatar modal for approach explanation
- Approach evaluation using DeepSeek / Ollama
- Monaco code editor
- In-browser Python execution with Pyodide
- Expected vs actual output test validation
- Live camera proctoring
- Anti-cheating checks
- Approach vs code consistency evaluation

---

## Features

### Candidate Experience
- View coding problem and test cases
- Start interview in an AI avatar modal
- Speak out approach using browser speech recognition
- Get AI evaluation on approach before coding
- Unlock editor only after approach approval
- Write Python code in Monaco editor
- Run code against test cases
- See expected output and actual output
- Get score based on passed tests

### AI Evaluation
- Candidate approach evaluated by DeepSeek via Ollama
- Strict scoring from `0` to `10`
- Editor unlocks only if score is greater than `6`
- Approach and code can be compared for consistency

### Proctoring
- Camera access
- Tab switch detection
- Copy prevention
- Full interview style experience

---

## Tech Stack

### Frontend
- React
- Material UI
- Monaco Editor
- Pyodide
- Web Speech API

### Backend
- Flask
- Ollama
- DeepSeek Coder model
- SQLAlchemy

---

## Project Structure

```bash
project-root/
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   └── AssessmentPlayerPage.jsx
│   │   └── ...
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   └── candidate_transcript.py
│   │   ├── models/
│   │   │   └── ollamma.py
│   │   └── ...
│   ├── run.py
│   └── requirements.txt
│
└── README.md