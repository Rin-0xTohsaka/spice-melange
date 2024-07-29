import os
import pandas as pd
from jinja2 import Template
from .fetch_data import fetch_data

def process_market_data():
    endpoint = "/public/coins/wif/v1"
    data = fetch_data(endpoint)
    df = pd.DataFrame([data['data']])
    return df

def generate_market_data_charts(df):
    os.makedirs('charts', exist_ok=True)

    # HTML Template for Chart.js and DataTables with additional descriptions
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Market Data</title>
        <link rel="stylesheet" href="https://cdn.datatables.net/1.10.21/css/jquery.dataTables.min.css">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://code.jquery.com/jquery-3.5.1.js"></script>
        <script src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.min.js"></script>
        <style>
            .tooltip {
                position: relative;
                display: inline-block;
                cursor: pointer;
            }
            .tooltip .tooltiptext {
                visibility: hidden;
                width: 200px;
                background-color: black;
                color: #fff;
                text-align: center;
                border-radius: 6px;
                padding: 5px;
                position: absolute;
                z-index: 1;
                bottom: 125%; /* Position the tooltip above the text */
                left: 50%;
                margin-left: -100px;
                opacity: 0;
                transition: opacity 0.3s;
            }
            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }
        </style>
    </head>
    <body>
        <h1>Market Data</h1>
        <div class="tooltip">Market Cap
            <span class="tooltiptext">Total dollar market value of all circulating supply or outstanding shares</span>
        </div>
        <canvas id="marketCapChart"></canvas>
        <script>
            var ctx = document.getElementById('marketCapChart').getContext('2d');
            var marketCapChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Market Cap'],
                    datasets: [{
                        label: 'Market Cap (USD)',
                        data: [{{ market_cap }}],
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Market Cap (USD)'
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.dataset.label + ': $' + context.raw.toLocaleString();
                                }
                            }
                        }
                    }
                }
            });
        </script>

        <h1>Price and Volume Data</h1>
        <table id="priceVolumeTable" class="display">
            <thead>
                <tr>
                    <th>Price (USD)</th>
                    <th>24h Volume (USD)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>${{ price }}</td>
                    <td>${{ volume_24h }}</td>
                </tr>
            </tbody>
        </table>
        <script>
            $(document).ready(function() {
                $('#priceVolumeTable').DataTable();
            });
        </script>

        <h1>Percentage Changes</h1>
        <div class="tooltip">24h % Change
            <span class="tooltiptext">Percent change in price since 24 hours ago</span>
        </div>
        <div class="tooltip">7d % Change
            <span class="tooltiptext">Percent change in price since 7 days ago</span>
        </div>
        <canvas id="percentageChangesChart"></canvas>
        <script>
            var ctx2 = document.getElementById('percentageChangesChart').getContext('2d');
            var percentageChangesChart = new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: ['24h % Change', '7d % Change'],
                    datasets: [{
                        label: 'Percentage Change',
                        data: [{{ percent_change_24h }}, {{ percent_change_7d }}],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Percentage Change (%)'
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.dataset.label + ': ' + context.raw.toFixed(2) + '%';
                                }
                            }
                        }
                    }
                }
            });
        </script>
    </body>
    </html>
    """

    # Render HTML with data
    template = Template(html_template)
    html_content = template.render(
        market_cap=df['market_cap'][0],
        price=df['price'][0],
        volume_24h=df['volume_24h'][0],
        percent_change_24h=df['percent_change_24h'][0],
        percent_change_7d=df['percent_change_7d'][0]
    )

    # Save HTML to file
    with open(os.path.join('charts', 'market_data.html'), 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    df_market_data = process_market_data()
    generate_market_data_charts(df_market_data)
