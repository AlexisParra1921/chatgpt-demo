function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    document.getElementById("user-input").value = "";

    // Send the user input to the backend Python code
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "backend.php", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = xhr.responseText;
            addMessage("You", userInput);
            addMessage("Chatbot", response);
        }
    };
    xhr.send("query=" + userInput);
}

function addMessage(sender, message) {
    var chatHistory = document.getElementById("chat-history");
    var messageDiv = document.createElement("div");
    messageDiv.innerHTML = "<strong>" + sender + ":</strong> " + message;
    chatHistory.appendChild(messageDiv);
}
