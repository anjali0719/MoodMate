const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');

let messageId = 0;
let isProcessing = false;

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function addMessage(text, type = 'sent') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = `
                <div>${text}</div>
                <div class="message-time">${getCurrentTime()}</div>
            `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    messageId++;
}

function showTypingIndicator() {
    typingIndicator.style.display = 'block';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

function setInputEnabled(enabled) {
    chatInput.disabled = !enabled;
    sendButton.disabled = !enabled;
    
    if (enabled) {
        sendButton.style.opacity = '1';
        sendButton.style.cursor = 'pointer';
        chatInput.focus();
    } else {
        sendButton.style.opacity = '0.6';
        sendButton.style.cursor = 'not-allowed';
    }
}

async function sendMessage() {
    const message = chatInput.value.trim();
    if (message === '' || isProcessing) return;

    // Add user message
    isProcessing = true;
    setInputEnabled(false);
    addMessage(message, 'sent');
    chatInput.value = '';

    // Show typing indicator and simulate response
    showTypingIndicator();


    try {
        const response = await fetch('/api/v1/analyze-mood/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: message })
        });
        const data = await response.json();
        hideTypingIndicator();

        if (data.error) {
            addMessage(`Error: ${data.response}`, 'received');
        } else {
            addMessage(data.response, 'received');
            
            // Optional: Update page title with journal title
            if (data.journal_title) {
                document.title = `Chat - ${data.journal_title}`;
            }
        }
    } catch (error) {
        hideTypingIndicator();
        console.error('Error:', error);
        addMessage("Sorry, something went wrong. Please try again later.", 'received');
    } finally {
        isProcessing = false;
        setInputEnabled(true);
    }
}

// Event listeners
sendButton.addEventListener('click', sendMessage);

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

chatInput.addEventListener('input', (e) => {
    // Visual feedback for send button
    if (e.target.value.trim().length > 0 && !isProcessing) {
        sendButton.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        sendButton.style.transform = 'scale(1.05)';
    } else {
        sendButton.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        sendButton.style.transform = 'scale(1)';
    }
});

// Auto-resize textarea for longer messages
chatInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Focus on input when page loads
document.addEventListener('DOMContentLoaded', function() {
    chatInput.focus();
});

const sidebar = document.getElementById('sidebar');
const toggle = document.getElementById('sidebarToggle');
toggle.addEventListener('click', () => {
    sidebar.classList.toggle('expanded');
    document.body.classList.toggle('sidebar-open');
});

document.querySelectorAll('.chat-navigation').forEach(btn => {
  btn.addEventListener('click', function() {
    const chatId = this.getAttribute('data-chat-id');
    fetch(`/chat/${chatId}`)
      .then(response => response.json())
      .then(data => {
        // Assuming data.messages is an array of message objects
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = '';
        data.messages.forEach(msg => {
          const msgDiv = document.createElement('div');
          msgDiv.className = msg.sent ? 'message sent' : 'message received';
          msgDiv.innerHTML = `<div>${msg.text}</div>`;
          chatMessages.appendChild(msgDiv);
        });
      });
  });
});