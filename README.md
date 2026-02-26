<p align="center">
  <img src="https://cdn.discordapp.com/avatars/1475949970711380069/f3c6ac73186035b46e4a32a067bc72f1.png?size=1024" width="180" height="180" style="border-radius:50%;">
</p>

<h1 align="center">🤖 VOTOX</h1>

<p align="center">
  Powerful • Modular • Secure Discord Bot
</p>

---

## ✨ Overview

**VOTOX** is a feature-rich Discord bot focused on:

- 🛡️ Server protection (AntiNuke & AntiRaid)
- 🧰 Use SQLite
- ⚙️ Modular command system using Cogs
- 🔄 Dynamic rotating bot presence
- 🧰 Utility commands
- 🎉 Fun & interactive features
- 📈 Scalable and organized structure

The bot is built for flexibility and easy expansion.

---

## 🚀 Features

### 🛡️ Protection System
- Anti-nuke system
- Anti-raid detection
- Channel & role protection
- Logging system support

### ⚙️ Modular Architecture
- Clean Cog-based structure
- Easy to add or remove modules
- Organized command categories

### 🧰 Utilities
- Server info commands
- Admin tools
- Helper commands
- Ping responder

### 🎮 Fun Commands
- Interactive commands
- Entertainment features
- Custom responses

### 🔄 Dynamic Presence
- Rotating activity messages
- Listening / Watching / Custom statuses
- Updates every few seconds

---

## 📦 Requirements

Make sure you have:

- Python **3.8+**
- A Discord Bot Token
- Required Python packages

### Dependencies

```
discord.py
aiohttp
```

Install them with:

```bash
pip install -r requirements.txt
```

---

## ⚡ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/phasedev-oxiodev/VOTOX.git
cd VOTOX
```

### 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 3️⃣ Create a Discord Bot

1. Go to the **Discord Developer Portal**
2. Click **New Application**
3. Go to **Bot**
4. Click **Add Bot**
5. Copy your **Bot Token**

---

### 4️⃣ Configure the Bot

Open `main.py` and replace:

```python
TOKEN = "YOUR_BOT_TOKEN"
```

With your real token:

```python
TOKEN = "YOUR_REAL_TOKEN_HERE"
```

⚠️ **Never share your token publicly.**

---

### 5️⃣ Run the Bot

```bash
python main.py
```

If everything is correct, your bot will come online 🎉

---

## 📁 Project Structure

```
VOTOX/
│
├── cogs/
│   ├── admin.py
│   ├── help.py
│   ├── fun.py
│   ├── world.py
│   ├── utilities.py
│   ├── antinuke.py
│   ├── antiraid.py
│   ├── server.py
│   └── PingResponder.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## 🧠 How The Cog System Works

Each file inside the `cogs/` folder contains:

- A command group
- A category of features
- Setup functions for loading

To add a new feature:

1. Create a new file inside `cogs/`
2. Define a Cog class
3. Load it inside `main.py`

Example:

```python
await bot.load_extension("cogs.mynewcog")
```

---

## 🔐 Security Recommendations

For better security:

- Use a `.env` file for storing your token
- Add permission checks for admin commands
- Restrict sensitive commands to trusted roles
- Add error handling for stability

Example `.env` usage:

```python
import os
TOKEN = os.getenv("TOKEN")
```

---

## 🛠️ Customization

You can easily customize:

- Bot prefix
- Status messages
- Cog loading order
- Command permissions
- Logging system
- Embed styling

---

## 📊 Future Improvements (Ideas)

- Ticket system
- Economy system
- Level system
- Webhook logging

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Open a Pull Request


---

## 👑 Author

Developed by **PhaseDev**

If you like this project, consider giving it a ⭐ on GitHub!

---

# 💎 VOTOX – Powerful. Modular. Secure.
