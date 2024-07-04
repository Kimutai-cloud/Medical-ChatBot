async function sendQuestion() {
    const userInput = document.getElementById('user-input').value;
    const response = await fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: userInput })
    });
    const data = await response.json();
    const chatBox = document.getElementById('chat-box');
    const responseId = `response-${Date.now()}`;

    const userMessage = document.createElement('div');
    userMessage.classList.add('user-message');
    userMessage.innerHTML = `
        <p>${userInput}</p>
    `;
    chatBox.appendChild(userMessage);

    const botMessage = document.createElement('div');
    botMessage.classList.add('bot-message');
    botMessage.innerHTML = `
        <p>${data.answer}</p>
        <button class="feedback-btn" onclick="sendFeedback('${responseId}', 'up')">👍</button>
        <button class="feedback-btn" onclick="sendFeedback('${responseId}', 'down')">👎</button>
    `;
    chatBox.appendChild(botMessage);

    const responseElement = document.createElement('p');
    responseElement.id = responseId;
    responseElement.style.display = 'none';
    responseElement.textContent = data.answer;
    chatBox.appendChild(responseElement);

    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendFeedback(responseId, feedback) {
    const responseElement = document.getElementById(responseId);
    const answer = responseElement.textContent;

    const response = await fetch('/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ answer: answer, feedback: feedback })
    });
    const data = await response.json();
    const chatBox = document.getElementById('chat-box');

    const feedbackMessage = document.createElement('div');
    feedbackMessage.classList.add('bot-message');
    if (data.status === "Feedback received") {
        feedbackMessage.textContent = `Feedback received: ${feedback === 'up' ? '👍' : '👎'}`;
    } else {
        feedbackMessage.textContent = `Failed to submit feedback.`;
    }
    chatBox.appendChild(feedbackMessage);

    chatBox.scrollTop = chatBox.scrollHeight;
}
