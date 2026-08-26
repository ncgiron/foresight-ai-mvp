
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

import json

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from plotly.utils import PlotlyJSONEncoder
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

    cpu_plot = json.dumps(
        cpu_fig.to_plotly_json(),
        cls=PlotlyJSONEncoder
    )
    sessions_plot = json.dumps(
        sessions_fig.to_plotly_json(),
        cls=PlotlyJSONEncoder
    )
    latency_plot = json.dumps(
        latency_fig.to_plotly_json(),
        cls=PlotlyJSONEncoder
    )
    throughput_plot = json.dumps(
        throughput_fig.to_plotly_json(),
        cls=PlotlyJSONEncoder
    )

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

                    .plot-container {{
                        width: 100%;
                        min-height: 420px;
                        height: 45vh;
                        max-height: 520px;
                    }}

                    .card h2 {{
                        margin-bottom: 16px;
                    }}

                    .control-row {{
                        display: flex;
                        gap: 8px;
                        align-items: center;
                        flex-wrap: wrap;
                    }}
                    
            

        </style>

        <script src="https://cdn.plot.ly/plotly-3.7.0.min.js"></script>

    </head>

    <script>
    async function askAI() {{
        const question = document.getElementById("question").value;

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

    async function loadScenarios() {{
        const res = await fetch('/scenario/list');
        const data = await res.json();
        const sel = document.getElementById('scenario-select');
        sel.innerHTML = '';
        data.scenarios.forEach(s => {{
            const opt = document.createElement('option');
            opt.value = s.name;
            opt.text = `${{s.name}} — ${{s.description}}`;
            sel.appendChild(opt);
        }});
    }}

    async function setScenario() {{
        const sel = document.getElementById('scenario-select');
        const name = sel.value || null;

        await fetch('/scenario/set', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ scenario: name }})
        }});

        refreshCurrentScenario();
        loadTimeseries().catch(console.error);
    }}

    async function clearScenario() {{
        await fetch('/scenario/set', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ scenario: null }})
        }});
        refreshCurrentScenario();
        loadTimeseries().catch(console.error);
    }}

    async function refreshCurrentScenario() {{
        const res = await fetch('/scenario/current');
        const data = await res.json();
        const status = document.getElementById('scenario-status');
        status.innerText = data.scenario ? `Active: ${{data.scenario}}` : 'No active scenario';
    }}

    function buildTraces(timeseries, metric, yaxisTitle) {{
        return Object.keys(timeseries).map(node => {{
            const values = timeseries[node];
            return {{
                x: values.map(sample => sample.timestamp),
                y: values.map(sample => sample[metric]),
                mode: 'lines',
                name: node,
                line: {{ shape: 'spline', smoothing: 1.3, width: 2 }},
                marker: {{ size: 2 }}
            }};
        }});
    }}

    const chartConfig = {{
        responsive: true,
        displayModeBar: false,
        scrollZoom: true
    }};

    function updateCharts(timeseries) {{
        const commonLayout = {{
            autosize: true,
            margin: {{ t: 40, l: 60, r: 20, b: 50 }},
            legend: {{ orientation: 'h', y: -0.2 }},
            xaxis: {{ title: 'Time', type: 'date', tickformat: '%b %d %H:%M' }},
            yaxis: {{ rangemode: 'tozero', automargin: true }},
            hovermode: 'x unified'
        }};

        Plotly.react('cpu-chart', buildTraces(timeseries, 'cpu_usage'), {{
            ...commonLayout,
            title: 'CPU Usage per Network Function',
            yaxis: {{ ...commonLayout.yaxis, title: 'CPU (%)', fixedrange: false }}
        }}, chartConfig);

        Plotly.react('sessions-chart', buildTraces(timeseries, 'sessions'), {{
            ...commonLayout,
            title: 'Active Sessions',
            yaxis: {{ ...commonLayout.yaxis, title: 'Sessions', fixedrange: false }}
        }}, chartConfig);

        Plotly.react('latency-chart', buildTraces(timeseries, 'latency_ms'), {{
            ...commonLayout,
            title: 'Latency per Network Function',
            yaxis: {{ ...commonLayout.yaxis, title: 'Latency (ms)', fixedrange: false }}
        }}, chartConfig);

        Plotly.react('throughput-chart', buildTraces(timeseries, 'throughput_mbps'), {{
            ...commonLayout,
            title: 'Network Throughput',
            yaxis: {{ ...commonLayout.yaxis, title: 'Throughput (Mbps)', fixedrange: false }}
        }}, chartConfig);
    }}

    async function loadTimeseries() {{
        const interval = parseInt(document.getElementById('refresh-interval').value, 10);
        const url = `/kpi/timeseries?minutes=${{interval}}&days=7`;
        const res = await fetch(url, {{ cache: 'no-store' }});
        const data = await res.json();
        updateCharts(data.timeseries);
        const status = document.getElementById('refresh-status');
        status.innerText = `Last refreshed: ${{new Date().toLocaleTimeString()}}`;
    }}

    let refreshTimer = null;

    function startRefresh() {{
        if (refreshTimer) {{
            clearInterval(refreshTimer);
        }}
        const interval = parseInt(document.getElementById('refresh-interval').value, 10);
        loadTimeseries().catch(console.error);
        refreshTimer = setInterval(() => {{
            loadTimeseries().catch(console.error);
        }}, interval * 60 * 1000);
        document.getElementById('refresh-status').innerText = `Auto-refresh every ${{interval}} minute(s).`;
    }}

    function stopRefresh() {{
        if (refreshTimer) {{
            clearInterval(refreshTimer);
            refreshTimer = null;
        }}
        document.getElementById('refresh-status').innerText = 'Auto-refresh paused.';
    }}

    document.addEventListener('DOMContentLoaded', () => {{
        loadScenarios().catch(console.error);
        refreshCurrentScenario().catch(console.error);
        startRefresh();
    }});

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

            <div id="cpu-chart" class="plot-container"></div>

        </div>

        <div class="card">

            <h2>Sessions</h2>

            <div id="sessions-chart" class="plot-container"></div>

        </div>

        <div class="card">

            <h2>Latency</h2>

            <div id="latency-chart" class="plot-container"></div>

        </div>

        <div class="card">

            <h2>Throughput</h2>

            <div id="throughput-chart" class="plot-container"></div>

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

            <hr />

            <h2>Scenario Controls</h2>

            <select id="scenario-select" style="width:100%; padding:8px; margin-bottom:8px;"></select>

            <div style="display:flex; gap:8px;">
                <button onclick="setScenario()">Activate</button>
                <button onclick="clearScenario()" style="background:#e5e7eb;color:#111;">Clear</button>
            </div>

            <div id="scenario-status" style="margin-top:10px; color:#374151;">Loading scenarios...</div>

            <hr />

            <h2>Refresh Controls</h2>

            <div class="control-row">
                <label for="refresh-interval">Update every</label>
                <select id="refresh-interval" style="padding:8px;">
                    <option value="1">1 minute</option>
                    <option value="5" selected>5 minutes</option>
                    <option value="15">15 minutes</option>
                </select>
                <button onclick="startRefresh()">Start</button>
                <button onclick="stopRefresh()" style="background:#e5e7eb;color:#111;">Stop</button>
            </div>

            <div id="refresh-status" style="margin-top:10px; color:#374151;">Last refreshed: just now</div>

        </div>

    </div>

</div>
    </body>

    </html>
    """

    return HTMLResponse(content=html)