from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route("/")
def index():
    html = """
    <!doctype html>
    <html>
    <head>
        <title>System Health Metrics Dashboard</title>

        <!-- Chart.js CDN -->
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                padding: 30px;
            }
            h1 {
                color: #333;
            }
            .chart-container {
                width: 600px;
                margin-bottom: 40px;
            }
        </style>
    </head>

    <body>
        <h1>System Health Dashboard</h1>

        <div class="chart-container">
            <h3>CPU Usage (%)</h3>
            <canvas id="cpuChart"></canvas>
        </div>

        <div class="chart-container">
            <h3>Memory Usage (%)</h3>
            <canvas id="memoryChart"></canvas>
        </div>

        <script>
            const cpuCtx = document.getElementById('cpuChart').getContext('2d');
            const memoryCtx = document.getElementById('memoryChart').getContext('2d');

            const cpuChart = new Chart(cpuCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'CPU %',
                        data: [],
                        borderWidth: 2
                    }]
                },
                options: { responsive: true }
            });

            const memoryChart = new Chart(memoryCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Memory %',
                        data: [],
                        borderWidth: 2
                    }]
                },
                options: { responsive: true }
            });

            function fetchData() {
                fetch('/metrics')
                    .then(response => response.json())
                    .then(data => {
                        const time = new Date().toLocaleTimeString();

                        cpuChart.data.labels.push(time);
                        cpuChart.data.datasets[0].data.push(data.cpu);

                        memoryChart.data.labels.push(time);
                        memoryChart.data.datasets[0].data.push(data.memory);

                        cpuChart.update();
                        memoryChart.update();
                    });
            }

            setInterval(fetchData, 2000); // update every 2 seconds
        </script>
    </body>
    </html>
    """

    return html


@app.route("/metrics")
def metrics():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    return jsonify({"cpu": cpu, "memory": memory})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
