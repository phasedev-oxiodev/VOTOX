<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VOTOX - Powerful Modular Discord Bot</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #0f0f0f, #1c1c2e);
    color: #ffffff;
    line-height: 1.6;
}

.container {
    max-width: 1100px;
    margin: auto;
    padding: 40px 20px;
}

header {
    text-align: center;
    padding: 60px 20px;
}

header img {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    border: 4px solid #5865F2;
    box-shadow: 0 0 40px rgba(88,101,242,0.6);
}

h1 {
    font-size: 3rem;
    margin-top: 20px;
    color: #5865F2;
}

.subtitle {
    font-size: 1.2rem;
    opacity: 0.8;
}

.section {
    margin-top: 60px;
}

.section h2 {
    font-size: 2rem;
    margin-bottom: 20px;
    border-left: 4px solid #5865F2;
    padding-left: 15px;
}

.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.card {
    background: #1f1f35;
    padding: 20px;
    border-radius: 12px;
    transition: 0.3s;
    border: 1px solid rgba(255,255,255,0.05);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(88,101,242,0.3);
}

.code-block {
    background: #111;
    padding: 15px;
    border-radius: 8px;
    font-family: monospace;
    margin-top: 10px;
    overflow-x: auto;
}

.btn {
    display: inline-block;
    margin-top: 20px;
    padding: 12px 25px;
    background: #5865F2;
    color: white;
    text-decoration: none;
    border-radius: 8px;
    transition: 0.3s;
}

.btn:hover {
    background: #4752c4;
}

footer {
    text-align: center;
    padding: 40px;
    opacity: 0.6;
    margin-top: 60px;
}
</style>
</head>

<body>

<header>
    <img src="https://cdn.discordapp.com/avatars/1475949970711380069/f3c6ac73186035b46e4a32a067bc72f1.png?size=1024" alt="VOTOX Logo">
    <h1>🤖 VOTOX</h1>
    <p class="subtitle">Powerful • Modular • Secure Discord Bot</p>
    <a href="https://github.com/phasedev-oxiodev/VOTOX" class="btn">View on GitHub</a>
</header>

<div class="container">

    <div class="section">
        <h2>✨ Features</h2>
        <div class="features">
            <div class="card">
                <h3>🛡️ Protection System</h3>
                <p>Channel & role protection with advanced logging support.</p>
            </div>

            <div class="card">
                <h3>⚙️ Modular Architecture</h3>
                <p>Clean Cog-based structure. Easily expandable system.</p>
            </div>

            <div class="card">
                <h3>🎮 Fun Commands</h3>
                <p>Interactive entertainment and custom responses.</p>
            </div>

            <div class="card">
                <h3>🔄 Dynamic Presence</h3>
                <p>Rotating bot status (Watching / Listening / Custom).</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>⚡ Installation</h2>
        <div class="code-block">
git clone https://github.com/phasedev-oxiodev/VOTOX.git
cd VOTOX
pip install -r requirements.txt
python main.py
        </div>
    </div>

    <div class="section">
        <h2>📁 Project Structure</h2>
        <div class="code-block">
VOTOX/
│
├── cogs/
├── main.py
├── requirements.txt
└── README.md
        </div>
    </div>

    <div class="section">
        <h2>🔐 Security Tips</h2>
        <ul>
            <li>Use .env file for tokens</li>
            <li>Restrict admin commands</li>
            <li>Add error handling</li>
            <li>Never share your token</li>
        </ul>
    </div>

</div>

<footer>
    👑 Developed by PhaseDev • VOTOX © 2026
</footer>

</body>
</html>
