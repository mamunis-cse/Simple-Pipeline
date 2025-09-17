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
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            font-family: 'Arial', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            color: #fff;
        }
        h1 {
            font-size: 4em; /* Bigger title */
            background: linear-gradient(90deg, #f12711, #f5af19);
            padding: 40px 60px;
            border-radius: 25px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
            animation: glow 2s ease-in-out infinite alternate, fadeIn 2s ease-in-out;
            text-align: center;
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
    <h1>🚀 CI/CD with Docker 🎉</h1>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


