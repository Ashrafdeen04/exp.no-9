from flask import Flask
import psutil

app = Flask(__name__)

@app.route("/")
def index():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    html = f"""
    <!doctype html>
    <html>
    <head>
        <title>System Health Metrics</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                padding: 30px;
            }}
            h1 {{
                color: #333;
            }}
            .metric {{
                font-size: 20px;
                margin-bottom: 15px;
            }}
        </style>
    </head>
    <body>
        <h1>Flask System Health Dashboard</h1>
        <p class="metric"><strong>CPU Usage:</strong> {cpu}%</p>
        <p class="metric"><strong>Memory Usage:</strong> {memory}%</p>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
