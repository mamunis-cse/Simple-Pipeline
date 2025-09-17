from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🚀 CI/CD with Docker</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Arial', sans-serif;
        }
        .container {
            text-align: center;
            color: #fff;
        }
        h1 {
            font-size: 5em;
            margin: 0.2em 0;
            background: linear-gradient(90deg, #f12711, #f5af19);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 2s ease-in-out infinite alternate, fadeIn 2s ease-in-out;
        }
        h2 {
            font-size: 3em;
            margin: 0.2em 0;
            color: #00f0ff;
            animation: fadeIn 3s ease-in-out;
        }
        h3 {
            font-size: 2em;
            margin: 0.2em 0;
            color: #ff69b4;
            animation: fadeIn 4s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes glow {
            from { text-shadow: 0 0 10px #f12711, 0 0 20px #f5af19; }
            to { text-shadow: 0 0 20px #f12711, 0 0 40px #f5af19; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 CI/CD</h1>
        <h2>with Docker</h2>
        <h3>Automate, Build, Deploy, Repeat!</h3>
        <h3>Containerized & Ready for Lab</h3>
        <h3>Flask + Docker + GitHub Actions</h3>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
