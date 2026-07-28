
"""
===========================================================
Dashboard Endpoints

Purpose
-------
Provides human-friendly telecom KPI visualizations.

The REST APIs remain machine-oriented and return JSON.

The dashboard endpoints render interactive Plotly charts
for engineers and demonstrations.

Current Visualizations
----------------------
- CPU Usage
- Active Sessions
- Latency
- Throughput

Future Enhancements
-------------------
- AI anomaly highlighting
- Correlation view
- Root cause analysis panel
- Capacity forecasting
===========================================================
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from dashboard.summary import calculate_summary

from mock.kpi_generator import generate_timeseries
from services.foresight_engine import build_foresight_context

from dashboard.plots import (
    cpu_chart,
    sessions_chart,
    latency_chart,
    throughput_chart
)



router = APIRouter()



@router.get("/dashboard/timeseries", response_class=HTMLResponse)
def dashboard_timeseries():
    """
    Generates a complete telecom KPI dashboard.

    Workflow
    --------
    1. Generate simulated time-series KPI data
    2. Create Plotly figures for each KPI
    3. Embed figures into a single HTML page
    4. Return dashboard to browser

    Returns
    -------
    HTMLResponse
        Interactive telecom KPI dashboard.
    """
    from app.routes import build_anomalies
    from services.forecast_engine import forecast_network

    anomalies = build_anomalies()

    historical = generate_timeseries(72)

    foresight = build_foresight_context(
        anomalies,
        historical["timeseries"]
    )
    # Generate network KPI history
    data = generate_timeseries()

    # Extract time-series data section
    timeseries = data["timeseries"]

    # Calculate dashboard summary statistics
    summary = calculate_summary(timeseries)

    
    health_rows = ""

    for node, metrics in foresight["anomalies"].items():

        risk = "LOW"

        for metric in metrics.values():

            if metric.get("risk") == "HIGH":
                risk = "HIGH"
                break

        icon = {
            "LOW": "🟢",
            "MEDIUM": "🟡",
            "HIGH": "🔴"
        }.get(risk, "🟢")

        health_rows += f"""
        <tr>
            <td><strong>{node}</strong></td>
            <td>{icon} {risk}</td>
        </tr>
        """
    
    
    
    # Build individual KPI charts
    cpu_fig = cpu_chart(timeseries)
    sessions_fig = sessions_chart(timeseries)
    latency_fig = latency_chart(timeseries)
    throughput_fig = throughput_chart(timeseries)

    # Build dashboard HTML
    html = f"""
    <html>

    <head>

        <title>Telecom AI Dashboard</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}

            h1 {{
                text-align: center;
                color: #1f2937;
            }}

            h2 {{
                color: #1f2937;
            }}

            .card {{
                background: white;
                padding: 20px;
                margin-bottom: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}

            .summary {{
                background: white;
                padding: 20px;
                margin-top: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            td {{
                padding: 8px;
                border-bottom: 1px solid #e5e7eb;
            }}
            
            
            
            .dashboard-container {{
                        display: flex;
                        gap: 20px;
                    }}

                    .left-panel {{
                        width: 70%;
                    }}

                    .right-panel {{
                        width: 30%;
                    }}

                    .copilot-panel {{
                        background: white;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                        position: sticky;
                        top: 20px;
                    }}

                    textarea {{
                        width: 100%;
                        min-height: 120px;
                        padding: 10px;
                        border-radius: 8px;
                        border: 1px solid #ccc;
                    }}

                    button {{
                        margin-top: 10px;
                        padding: 10px 20px;
                        background: #2563eb;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        cursor: pointer;
                    }}

                    button:hover {{
                        background: #1d4ed8;
                    }}

                    #ai-response {{
                        margin-top: 20px;
                        white-space: pre-wrap;
                        background: #f3f4f6;
                        padding: 10px;
                        border-radius: 8px;
                    }}
                    
            

        </style>

    </head>
<script>

async function askAI() {{

    const question =
        document.getElementById("question").value;

    const response = await fetch(
        "/copilot/ask",
        {{
            method: "POST",
            headers: {{
                "Content-Type": "application/json"
            }},
            body: JSON.stringify({{
                question: question
            }})
        }}
    );

    const data = await response.json();

    document.getElementById(
        "ai-response"
    ).innerText = data.answer;
}}

</script>
    <body>

        <h1>Telecom AI Dashboard</h1>
        
        <div class="dashboard-container">

            <div class="left-panel">

        <!-- Future integration with telecom_engine.py -->
        <div class="summary">

            <h2>Current Network Health</h2>

            <table>

                {health_rows}

            </table>

        </div>

        <div class="card">

            <h2>CPU Usage</h2>

            {cpu_fig.to_html(
                full_html=False,
                include_plotlyjs="cdn"
            )}

        </div>

        <div class="card">

            <h2>Sessions</h2>

            {sessions_fig.to_html(
                full_html=False,
                include_plotlyjs=False
            )}

        </div>

        <div class="card">

            <h2>Latency</h2>

            {latency_fig.to_html(
                full_html=False,
                include_plotlyjs=False
            )}

        </div>

        <div class="card">

            <h2>Throughput</h2>

            {throughput_fig.to_html(
                full_html=False,
                include_plotlyjs=False
            )}

        </div>

        <div class="summary">

            <h2>Top KPI Summary</h2>

            <table>

                <tr>
                    <td><strong>Peak CPU</strong></td>
                    <td>{summary["peak_cpu"]:.1f}%</td>
                </tr>

                <tr>
                    <td><strong>Peak Sessions</strong></td>
                    <td>{summary["peak_sessions"]:,}</td>
                </tr>

                <tr>
                    <td><strong>Peak Throughput</strong></td>
                    <td>{summary["peak_throughput"]:.0f} Mbps</td>
                </tr>

                <tr>
                    <td><strong>Average Latency</strong></td>
                    <td>{summary["average_latency"]:.1f} ms</td>
                </tr>

            </table>

        </div>

            </div>

    <div class="right-panel">

        <div class="copilot-panel">

            <h2>AI Copilot</h2>

            <textarea
                id="question"
                placeholder="Ask about network health..."
            ></textarea>

            <button onclick="askAI()">
                Ask AI
            </button>

            <div id="ai-response">

                AI response will appear here.

            </div>

        </div>

    </div>

</div>
    </body>

    </html>
    """


    return HTMLResponse(content=html)