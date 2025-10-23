# NoPickles MVP

A simplified MVP version of NoPickles.ai - An AI-powered conversational order-taking system for fast food.

## Overview

This MVP demonstrates the core feature of the NoPickles platform: intelligent conversational order-taking with menu recommendations.

### Features

- 🤖 Conversational order interface
- 🍔 Dynamic menu with item recommendations
- 💬 Simple natural language processing for orders
- 📝 Order summary and confirmation
- 🎯 Context-aware upselling suggestions

## Tech Stack

- **Backend**: FastAPI (Python 3.12+)
- **Frontend**: HTML/CSS/JavaScript (vanilla)
- **Data**: In-memory storage (no database required)

## Setup

### Requirements

- Python 3.12 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/gitmvp-com/nopickles-mvp.git
cd nopickles-mvp
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. Start ordering! Try saying things like:
   - "I want a burger"
   - "Add fries"
   - "What drinks do you have?"
   - "Complete my order"

## API Documentation

Once the server is running, visit:
- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Project Structure

```
nopickles-mvp/
├── app/
│   ├── main.py           # FastAPI application entry point
│   ├── models.py         # Data models
│   ├── agent.py          # Order processing agent
│   └── menu.py           # Menu data and logic
├── static/
│   ├── index.html        # Customer interface
│   ├── styles.css        # Styling
│   └── app.js            # Frontend logic
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Differences from Full NoPickles Platform

This MVP focuses on the core conversational ordering feature. The full platform includes:

- C# Windows IoT kiosk frontend
- Advanced LLM integration with LangChain
- PyTorch-based personalization models
- Vector database (FAISS) for RAG
- MySQL persistent storage
- Face and voice recognition
- Manager dashboard and analytics
- Multi-kiosk deployment with Kubernetes

## License

MIT License

## Based On

This MVP is based on [iota-tec/nopickles](https://github.com/iota-tec/nopickles)