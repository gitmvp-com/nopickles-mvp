"""FastAPI main application for NoPickles MVP"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import uuid

from app.models import Order, OrderItem, ConversationMessage, OrderResponse
from app.agent import OrderAgent
from app.menu import get_menu, get_menu_items

app = FastAPI(
    title="NoPickles MVP",
    description="AI-powered conversational order-taking system for fast food",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory storage for active sessions
sessions = {}


@app.get("/")
async def read_root():
    """Serve the main customer interface"""
    return FileResponse("static/index.html")


@app.get("/api/menu")
async def get_menu_endpoint():
    """Get the complete menu"""
    return get_menu()


@app.post("/api/session/start")
async def start_session():
    """Start a new order session"""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "agent": OrderAgent(),
        "order": Order(session_id=session_id, items=[], total=0.0)
    }
    return {
        "session_id": session_id,
        "message": "Welcome to NoPickles! What can I get for you today?"
    }


@app.post("/api/chat", response_model=OrderResponse)
async def chat(message: ConversationMessage):
    """Process a customer message and return response with order status"""
    if message.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found. Please start a new session.")
    
    session = sessions[message.session_id]
    agent = session["agent"]
    order = session["order"]
    
    # Process the message through the agent
    response = agent.process_message(message.message, order)
    
    return OrderResponse(
        message=response["message"],
        order=order,
        suggestions=response.get("suggestions", [])
    )


@app.post("/api/order/complete")
async def complete_order(session_id: str):
    """Complete and finalize the order"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    order = sessions[session_id]["order"]
    
    if not order.items:
        raise HTTPException(status_code=400, detail="Cannot complete an empty order")
    
    # In a real system, this would save to database and process payment
    order_summary = {
        "order_id": order.session_id,
        "items": [item.dict() for item in order.items],
        "total": order.total,
        "status": "confirmed"
    }
    
    # Clean up session
    del sessions[session_id]
    
    return order_summary


@app.delete("/api/session/{session_id}")
async def end_session(session_id: str):
    """End a session without completing the order"""
    if session_id in sessions:
        del sessions[session_id]
    return {"message": "Session ended"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "active_sessions": len(sessions)}
