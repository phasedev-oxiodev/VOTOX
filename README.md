# 🤖 VOTOX

<p align="center">
  <img src="https://cdn.discordapp.com/avatars/1475949970711380069/f3c6ac73186035b46e4a32a067bc72f1.png?size=1024" width="180" height="180">
</p>

<p align="center">
  <b>Powerful • Modular • Secure Discord Bot</b>
</p>

---

## ✨ Overview

**VOTOX** is a feature-rich Discord bot built using discord.py.

It focuses on:

- 🧰 SQLite integration  
- ⚙️ Modular Cog-based architecture  
- 🔄 Dynamic rotating presence  
- 🛡️ Protection systems  
- 🎮 Fun & interactive commands  
- 📈 Scalable and organized structure  

Built for flexibility and future expansion.

---

## 🚀 Features

### 🛡️ Protection System
- Channel protection  
- Role protection  
- Logging support  

### ⚙️ Modular Architecture
- Clean Cog system  
- Easy to add/remove modules  
- Organized command categories  

### 🧰 Utilities
- Server info  
- Admin tools  
- Helper commands  
- Ping responder  

### 🎮 Fun Commands
- Interactive features  
- Entertainment commands  
- Custom responses  

### 🔄 Dynamic Presence
- Rotating status messages  
- Watching / Listening / Custom  
- Auto-updating every few seconds  

---

## 📦 Requirements

- Python 3.8+
- Discord Bot Token
- Required dependencies

### Dependencies

```
discord.py
aiohttp
```

Install with:

```
pip install -r requirements.txt
```

---

## ⚡ Installation Guide

### 1️⃣ Clone the Repository

```
git clone https://github.com/phasedev-oxiodev/VOTOX.git
cd VOTOX
```

### 2️⃣ Install Requirements

```
pip install -r requirements.txt
```

### 3️⃣ Create a Discord Bot

1. Go to the Discord Developer Portal  
2. Click New Application  
3. Go to Bot  
4. Click Add Bot  
5. Copy your Bot Token  

---

### 4️⃣ Configure the Bot

Open `main.py` and replace:

```python
TOKEN = "TOKEN_NiGGER"
```

⚠️ Never share your token publicly.

---

### 5️⃣ Run the Bot

```
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

## 🔐 Security Recommendations

- Use a .env file for tokens  
- Restrict admin commands  
- Add permission checks  
- Add proper error handling  
- Never hardcode sensitive data  

---

## 🤝 Contributing

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
