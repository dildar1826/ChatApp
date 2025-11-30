let socket;
let currentUser = null;

// ----- LOGIN -----
async function login() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!username || !password) return alert("Enter username & password");

  // Call backend to create user
  const res = await fetch("http://localhost:5001/create-account", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  if (data.error) return alert(data.error);

  currentUser = username;
  document.getElementById("login-section").classList.add("hidden");
  document.getElementById("chat-section").classList.remove("hidden");

  connectSocket();
}

// ----- SOCKET.IO -----
function connectSocket() {
  socket = io("http://localhost:5001");

  socket.on("connect", () => console.log("Connected to server"));

  socket.on("receiveMessage", (msgData) => {
    addMessage(msgData.username, msgData.message, msgData.timestamp || new Date().toLocaleTimeString());
  });
}

// ----- SEND MESSAGE -----
function sendMessage() {
  const input = document.getElementById("messageInput");
  const message = input.value.trim();
  if (!message) return;

  const msgData = {
    username: currentUser,
    message,
    timestamp: new Date().toLocaleTimeString()
  };

  socket.emit("sendMessage", msgData);
  addMessage(currentUser, message, msgData.timestamp);
  input.value = "";
}

// ----- DISPLAY MESSAGE -----
function addMessage(username, message, time) {
  const messagesDiv = document.getElementById("messages");
  const msgBubble = `
    <div class="p-3 rounded-lg max-w-xs ${username===currentUser?'bg-blue-500 text-white ml-auto':'bg-gray-300 text-black mr-auto'}">
      <div class="font-semibold">${username}</div>
      <div>${message}</div>
      <div class="text-xs text-right opacity-70">${time}</div>
    </div>
  `;
  messagesDiv.innerHTML += msgBubble;
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
