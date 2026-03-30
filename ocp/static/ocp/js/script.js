/*
    Created By : Christian Merriman
    Date : 3/18/26
*/

//keeps track of the users chat history
let chatHistory = [];

//init our domcontent
document.addEventListener('DOMContentLoaded', () => {
    console.log("OCP Terminal Online...");
    const input = document.getElementById('ed-chat-user-input');
    const sendBtn = document.getElementById('ed-chat-send-btn');

    if(input){
        // Attach listeners FIRST (prevents the "click a bunch" issue)
        input.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') sendToEd209();
        });

        loadHistory();
    }

    if (sendBtn) {
        sendBtn.addEventListener('click', sendToEd209);
    }

    // Attempt to connect and pull history
    //checkConnectionAndLoad();

    // Check every 5 seconds to see if the server came back online
    //setInterval(checkConnectionAndLoad, 5000);
});

//load the chat history
async function loadHistory() {
    const display = document.getElementById('ed-chat-display-id');
    
    //give the user a visual cue that OCP is retrieving files
    display.innerHTML = '<div class="message ai-message">ACCESSING OCP ARCHIVES...</div>';

    try {
        const response = await fetch('/get_chat_history');
        const data = await response.json();
        
        //clear the "Loading" message and sync the data
        display.innerHTML = ''; 
        chatHistory = data.history;

        //render the historical directives
        chatHistory.forEach(msg => {
            //render message
            const cssClass = msg.role === 'user' ? 'user-message' : 'ai-message';
            display.innerHTML += `<div class="message ${cssClass}">${msg.content}</div>`;
            
            //set our time
            if (msg.timestamp) {
                display.innerHTML += `<div class="message date-message">${msg.timestamp}</div>`;
            }
        
        });

        scrollToBottom();

        updateChatConnectionStatus(true);

        console.log("Archive Sync Complete.");

    } catch (error) {
        display.innerHTML = '<div class="message ai-message">ERROR: ARCHIVE RETRIEVAL FAILED.</div>';
        updateChatConnectionStatus(false);
        console.error("Archive Error:", error);
    }
}

// will update if our chat is online or offline to html
function updateChatConnectionStatus(online){
    const statusText = document.getElementById('ed-chat-connection-status');
    if(online){
        // Update UI to Online
        statusText.innerText = "ONLINE";
        statusText.classList.remove('offline');
        statusText.classList.add('online');
    }
    else{
        // Server is still down
        statusText.innerText = "OFFLINE";
        statusText.classList.remove('online');
        statusText.classList.add('offline');
    }
}

//check our connection status to ed209 (local llama LLM)
async function checkConnectionAndLoad() {
    const statusText = document.getElementById('ed-chat-connection-status');
    
    try {
        const response = await fetch('http://127.0.0.1:8000/get_history');
        
        if (response.ok) {
            const data = await response.json();

            // If we were offline and now we're online, load the history
            if (statusText.classList.contains('offline')) {
                chatHistory = data.history || [];
                renderFullHistory();
            }

            // Update UI to Online
            statusText.innerText = "ONLINE";
            statusText.classList.remove('offline');
            statusText.classList.add('online');
        }
    } catch (error) {
        // Server is still down
        statusText.innerText = "OFFLINE";
        statusText.classList.remove('online');
        statusText.classList.add('offline');
    }
}

// Sends our chat message to ed209
async function sendToEd209() {
    const input = document.getElementById('ed-chat-user-input');
    const display = document.getElementById('ed-chat-display-id');
    const btnSend = document.getElementById('ed-chat-send-btn');
    

    const userText = input.value.trim();

    if (!userText) return; 

    //update the display message
    chatHistory.push({ role: "user", content: userText });
    display.innerHTML += `<div class="message user-message">${userText}</div>`;
    input.value = ""; 
    scrollToBottom();

    try {
        if(input){
            input.disabled = true
        }

        if(btnSend){
            btnSend.disabled = true;
        }
        
        //get the response from our LLM for ed209
        console.log('before fetch')
        const response = await fetch('/chat_ed209', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
             },
            body: JSON.stringify({ messages: chatHistory })
        });
        console.log('after fetch')
        const data = await response.json();
        console.log('after json')

        //got our data, so setup the html for it
        if (data.status === "success") {
            chatHistory = data.history;
            display.innerHTML += `<div class="message ai-message">${data.reply}</div>`;
            //set our time           
            display.innerHTML += `<div class="message date-message">${data.timestamp}</div>`;
          
        } else {
            display.innerHTML += `<div class="message ai-message">PROTOCOL ERROR: ${data.error}</div>`;
        }

        scrollToBottom();

        if(btnSend){
            btnSend.disabled = false;
        }

        if(input){
            input.disabled = false
        }

    } catch (error) {
        display.innerHTML += `<div class="message ai-message">ERROR: Could not connect to ED209.</div>`;
        scrollToBottom();

        if(btnSend){
            btnSend.disabled = false;
        }

        if(input){
            input.disabled = false
        }

    }
}

//will scroll to bottom of the chat
function scrollToBottom() {
    const display = document.getElementById('ed-chat-display-id');
    if (display) {
        display.scrollTop = display.scrollHeight;
    }
}

//goes through our chat history and renders to chat
function renderFullHistory() {
    const display = document.getElementById('ed-chat-display-id');
    if (!display) return;
    
    //clear it
    display.innerHTML = "";
    chatHistory.forEach(msg => {
        //if not a system message, then display on html
        if (msg.role !== 'system') {
            const cssClass = msg.role === 'user' ? 'user-message' : 'ai-message';
            display.innerHTML += `<div class="message ${cssClass}">${msg.content}</div>`;
        }
    });
    scrollToBottom();
}

//handles our security csrftoken for js
function getCookie(name) {
    let cookieValue = null;

    //make sure we have a cookie and take care of the csrftoken
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
