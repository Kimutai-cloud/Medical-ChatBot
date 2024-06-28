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
    chatBox.innerHTML += `<p>User: ${userInput}</p>`;
    chatBox.innerHTML += `<p>Bot: ${data.answer}</p>`;
}

async function uploadDataset() {
    const datasetInput = document.getElementById('dataset-input');
    const file = datasetInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    alert(data.status);
}
