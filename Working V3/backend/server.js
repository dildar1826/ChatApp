require("dotenv").config();
const express = require("express");
const http = require("http");
const cors = require("cors");
const { Server } = require("socket.io");
const supabase = require("./db"); // db.js connects to Supabase

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 5001;

const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: "*" },
});

// ---------- REST API ----------
app.post("/create-account", async (req, res) => {
  const { username, password } = req.body;

  if (!username || !password)
    return res.status(400).json({ error: "Username & password required" });

  // Insert user
  const { data, error } = await supabase.from("users").insert([
    { username, password }
  ]);

  if (error) return res.status(400).json({ error: error.message });

  res.json({ message: "User created", user: data });
});

// ---------- Socket.IO ----------
io.on("connection", (socket) => {
  console.log("A user connected:", socket.id);

  socket.on("sendMessage", async (msgData) => {
    console.log("Message received:", msgData);

    // Save to Supabase
    const { error } = await supabase.from("messages").insert([
      {
        username: msgData.username,
        content: msgData.message,
        created_at: new Date()
      }
    ]);

    if (error) console.log("DB insert error:", error.message);

    // Broadcast to all clients
    io.emit("receiveMessage", msgData);
  });

  socket.on("disconnect", () => {
    console.log("User disconnected:", socket.id);
  });
});

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
