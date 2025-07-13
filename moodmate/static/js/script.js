const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');

let messageId = 0;
let isProcessing = false;

// Sample auto-responses
// const autoResponses = [
//     "That's interesting! Tell me more 🤔",
//     "I totally agree with you! 👍",
//     "Wow, I hadn't thought about it that way 💭",
//     "That sounds amazing! 🎉",
//     "Thanks for sharing that with me 😊",
//     "I see what you mean 👀",
//     "That's a great point! 💡",
//     "Absolutely! 💯",
//     "I love your perspective on this 🌟",
//     "That made me smile 😄"
// ];

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

    // setTimeout(() => {
    //     hideTypingIndicator();
    //     const randomResponse = autoResponses[Math.floor(Math.random() * autoResponses.length)];
    //     addMessage(randomResponse, 'received');
    // }, 1000 + Math.random() * 2000); // Random delay between 1-3 seconds

    try {
        const response = await fetch('/analyze-mood', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: message })
        });
        const data = await response.json();
        hideTypingIndicator();
        addMessage(data.response, 'received');
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

// chatInput.addEventListener('keypress', (e) => {
//     if (e.key === 'Enter' && !e.shiftKey) {
//         e.preventDefault
//         sendMessage();
//     }
// });

// chatInput.addEventListener('input', (e) => {
//     if (e.target.value.length > 0) {
//         sendButton.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
//     } else {
//         sendButton.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
//     }
// });

// // Focus on input when page loads
// chatInput.focus();

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
