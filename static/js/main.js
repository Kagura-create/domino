function sendQuestion() {
    const questionInput = document.getElementById('question');
    const question = questionInput.value.trim();
    if (!question) return;

    const messagesDiv = document.getElementById('messages');
    const userMessage = document.createElement('div');
    userMessage.className = 'message user';
    userMessage.innerText = question;
    messagesDiv.appendChild(userMessage);

    questionInput.value = '';
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: question })
    })
    .then(response => response.json())
    .then(data => {
        if (data.response) {
            const dominoMessage = document.createElement('div');
            dominoMessage.className = 'message domino';
            dominoMessage.innerText = data.response;
            messagesDiv.appendChild(dominoMessage);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        } else {
            const errorMessage = document.createElement('div');
            errorMessage.className = 'message domino';
            errorMessage.innerText = 'Erreur : ' + data.error;
            messagesDiv.appendChild(errorMessage);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
    })
    .catch(error => {
        const errorMessage = document.createElement('div');
        errorMessage.className = 'message domino';
        errorMessage.innerText = 'Erreur : ' + error;
        messagesDiv.appendChild(errorMessage);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
}