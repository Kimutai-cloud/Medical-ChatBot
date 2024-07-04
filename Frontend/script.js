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
    chatBox.innerHTML += `<p class="user">User: ${userInput}</p>`;
    chatBox.innerHTML += `
        <p class="bot">
            Bot: ${data.answer}
            <br>
            <button onclick="sendFeedback('${responseId}', 'up')">👍</button>
            <button onclick="sendFeedback('${responseId}', 'down')">👎</button>
        </p>`;
    chatBox.innerHTML += `<p id="${responseId}" style="display: none;">${data.answer}</p>`;
    chatBox.scrollTop = chatBox.scrollHeight;  // Scroll to the bottom
}

async function sendFeedback(responseId, feedback) {
    const responseElement = document.getElementById(responseId);
    const answer = responseElement.innerText;

    const response = await fetch('/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ answer: answer, feedback: feedback })
    });
    const data = await response.json();
    const chatBox = document.getElementById('chat-box');

    if (data.status === "Feedback received") {
        chatBox.innerHTML += `<p class="bot">Feedback received: ${feedback === 'up' ? '👍' : '👎'}</p>`;
    } else {
        chatBox.innerHTML += `<p class="bot">Failed to submit feedback.</p>`;
    }
    chatBox.scrollTop = chatBox.scrollHeight;  // Scroll to the bottom
}
