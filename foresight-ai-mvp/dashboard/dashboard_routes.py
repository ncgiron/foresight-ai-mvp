
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

    # Generate network KPI history
    data = generate_timeseries()

    # Extract time-series data section
    timeseries = data["timeseries"]

    # Calculate dashboard summary statistics
    summary = calculate_summary(timeseries)

    # Build individual KPI charts
    cpu_fig = cpu_chart(timeseries)
    sessions_fig = sessions_chart(timeseries)
    latency_fig = latency_chart(timeseries)
    throughput_fig = throughput_chart(timeseries)

    # Compose dashboard HTML
    # html = f"""
    # <html>

    # <head>

    #     <title>Telecom AI Dashboard</title>

    #     <style>

    #         body {{
    #             font-family: Arial, sans-serif;
    #             margin: 20px;
    #             background-color: #f5f5f5;
    #         }}

    #         h1 {{
    #             text-align: center;
    #         }}

    #         .chart {{
    #             background: white;
    #             padding: 20px;
    #             margin-bottom: 30px;
    #             border-radius: 10px;
    #             box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    #         }}

    #     </style>

    # </head>

    # <hr>

    #     <h2>Top KPI Summary</h2>

    #     <div>

    #         <p>
    #             <strong>Peak CPU:</strong>
    #             {summary["peak_cpu"]:.1f}%
    #         </p>

    #         <p>
    #             <strong>Peak Sessions:</strong>
    #             {summary["peak_sessions"]:,}
    #         </p>

    #         <p>
    #             <strong>Peak Throughput:</strong>
    #             {summary["peak_throughput"]:.0f} Mbps
    #         </p>

    #         <p>
    #             <strong>Average Latency:</strong>
    #             {summary["average_latency"]:.1f} ms
    #         </p>

    #     </div>
    # <body>

    #     <h1>Telecom AI Dashboard</h1>

    #     <!-- CPU Utilisation -->
    #     <div class="chart">
    #         {cpu_fig.to_html(full_html=False, include_plotlyjs="cdn")}
    #     </div>

    #     <!-- Active Sessions -->
    #     <div class="chart">
    #         {sessions_fig.to_html(full_html=False, include_plotlyjs=False)}
    #     </div>

    #     <!-- Network Latency -->
    #     <div class="chart">
    #         {latency_fig.to_html(full_html=False, include_plotlyjs=False)}
    #     </div>

    #     <!-- Throughput -->
    #     <div class="chart">
    #         {throughput_fig.to_html(full_html=False, include_plotlyjs=False)}
    #     </div>

    # </body>

    # </html>
    # """


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

        </style>

    </head>

    <body>

        <h1>Telecom AI Dashboard</h1>

        <!-- Future integration with telecom_engine.py -->
        <div class="summary">

            <h2>Current Network Health</h2>

            <table>

                <tr>
                    <td><strong>AMF</strong></td>
                    <td>🟢 LOW</td>
                </tr>

                <tr>
                    <td><strong>SMF</strong></td>
                    <td>🟡 MEDIUM</td>
                </tr>

                <tr>
                    <td><strong>UPF</strong></td>
                    <td>🔴 HIGH</td>
                </tr>

                <tr>
                    <td><strong>PCF</strong></td>
                    <td>🟢 LOW</td>
                </tr>

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

    </body>

    </html>
    """


    return HTMLResponse(content=html)