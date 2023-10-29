// script.js

const sendButton = document.getElementById("sendButton");
const userInput = document.getElementById("userInput");
const chatBox = document.querySelector(".chat-box");

sendButton.addEventListener("click", function() {
    let inputText = userInput.value;
    let userMessageElement = document.createElement("div");
    userMessageElement.textContent = `Tu: ${inputText}`;
    chatBox.appendChild(userMessageElement);

    fetch("/chatbot/", {

        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: inputText })
    })
    .then(response => response.json())
    .then(data => {
        let botMessageElement = document.createElement("div");
        botMessageElement.textContent = `Aissociate: ${data.reply}`;
        chatBox.appendChild(botMessageElement);
    });
    
    userInput.value = "";
});
