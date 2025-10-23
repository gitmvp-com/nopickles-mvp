// NoPickles MVP - Frontend Application

let sessionId = null;
const API_BASE = '';

// DOM Elements
const chatBox = document.getElementById('chatBox');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const newOrderBtn = document.getElementById('newOrderBtn');
const completeOrderBtn = document.getElementById('completeOrderBtn');
const orderItems = document.getElementById('orderItems');
const orderTotal = document.getElementById('orderTotal');
const suggestionsContainer = document.getElementById('suggestions');

// Initialize
window.addEventListener('load', () => {
    startNewSession();
});

// Event Listeners
sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

newOrderBtn.addEventListener('click', () => {
    if (confirm('Start a new order? This will clear your current order.')) {
        startNewSession();
    }
});

completeOrderBtn.addEventListener('click', completeOrder);

// Functions
async function startNewSession() {
    try {
        const response = await fetch(`${API_BASE}/api/session/start`, {
            method: 'POST'
        });
        const data = await response.json();
        sessionId = data.session_id;
        
        // Clear chat and order
        chatBox.innerHTML = '';
        orderItems.innerHTML = '<p class="empty-order">Your order is empty</p>';
        orderTotal.textContent = '$0.00';
        completeOrderBtn.disabled = true;
        suggestionsContainer.innerHTML = '';
        
        // Add welcome message
        addMessage('bot', data.message);
        
    } catch (error) {
        console.error('Error starting session:', error);
        alert('Failed to start session. Please refresh the page.');
    }
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || !sessionId) return;
    
    // Add user message to chat
    addMessage('user', message);
    messageInput.value = '';
    
    try {
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                message: message
            })
        });
        
        const data = await response.json();
        
        // Add bot response
        addMessage('bot', data.message);
        
        // Update order display
        updateOrderDisplay(data.order);
        
        // Update suggestions
        updateSuggestions(data.suggestions);
        
    } catch (error) {
        console.error('Error sending message:', error);
        addMessage('bot', 'Sorry, I encountered an error. Please try again.');
    }
}

function addMessage(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const label = document.createElement('div');
    label.className = 'message-label';
    label.textContent = sender === 'bot' ? 'Assistant' : 'You';
    
    const content = document.createElement('div');
    content.textContent = text;
    
    messageDiv.appendChild(label);
    messageDiv.appendChild(content);
    chatBox.appendChild(messageDiv);
    
    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

function updateOrderDisplay(order) {
    if (!order.items || order.items.length === 0) {
        orderItems.innerHTML = '<p class="empty-order">Your order is empty</p>';
        orderTotal.textContent = '$0.00';
        completeOrderBtn.disabled = true;
        return;
    }
    
    orderItems.innerHTML = '';
    
    order.items.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'order-item';
        
        const itemTotal = (item.price * item.quantity).toFixed(2);
        
        itemDiv.innerHTML = `
            <div class="item-details">
                <div class="item-name">${item.name}</div>
                <div class="item-quantity">Quantity: ${item.quantity}</div>
            </div>
            <div class="item-price">$${itemTotal}</div>
        `;
        
        orderItems.appendChild(itemDiv);
    });
    
    orderTotal.textContent = `$${order.total.toFixed(2)}`;
    completeOrderBtn.disabled = false;
}

function updateSuggestions(suggestions) {
    suggestionsContainer.innerHTML = '';
    
    if (!suggestions || suggestions.length === 0) return;
    
    suggestions.forEach(suggestion => {
        const chip = document.createElement('button');
        chip.className = 'suggestion-chip';
        chip.textContent = suggestion;
        chip.addEventListener('click', () => {
            messageInput.value = suggestion;
            sendMessage();
        });
        suggestionsContainer.appendChild(chip);
    });
}

async function completeOrder() {
    if (!sessionId) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/order/complete?session_id=${sessionId}`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        // Show success message
        addMessage('bot', `Order confirmed! Your order total is $${data.total.toFixed(2)}. Thank you for choosing NoPickles!`);
        
        // Start new session
        setTimeout(() => {
            startNewSession();
        }, 2000);
        
    } catch (error) {
        console.error('Error completing order:', error);
        addMessage('bot', 'Sorry, there was an error completing your order. Please try again.');
    }
}
