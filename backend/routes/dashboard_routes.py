#Imports
from flask import Blueprint, render_template_string, current_app

# Create blueprint for dashboard routes
dashboard_bp = Blueprint('dashboard', __name__)

#Function to call the main dashboard
@dashboard_bp.route('/')
def dashboard_home():
    # Get quick stats
    try:
        recent_readings = current_app.db.get_recent_readings(hours=1)
        active_alerts = current_app.db.get_recent_alerts(hours=24)
        #As first, it will show the Stats, such as the total readings, the active alerts and the devices online
        stats = {
            "total_readings_today": len(recent_readings),
            "active_alerts": len([a for a in active_alerts if not a.get('resolved', False)]),
            "devices_online": len(set(r['device_id'] for r in recent_readings))
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        stats = {"total_readings_today": 0, "active_alerts": 0, "devices_online": 0}
    
    return render_template_string(DASHBOARD_HTML_TEMPLATE, stats=stats)

#HTML template (would be better to have it on another document, but I will do it so later on)
#Note for myself: Dont forget <-
#Also, I need to think more about the technology involved on front-end. (Frontend folder)
DASHBOARD_HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
    <head>
        <title>MAREA Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                margin: 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { 
                background: rgba(255,255,255,0.95); 
                padding: 20px; 
                border-radius: 15px; 
                margin-bottom: 20px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            }
            .stats { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 20px; 
                margin-bottom: 30px;
            }
            .stat-card { 
                background: rgba(255,255,255,0.9); 
                padding: 20px; 
                border-radius: 15px; 
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .stat-number { font-size: 2em; font-weight: bold; color: #2c3e50; }
            .stat-label { color: #7f8c8d; margin-top: 5px; }
            .cards { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
                gap: 20px; 
            }
            .card { 
                background: rgba(255,255,255,0.95); 
                padding: 20px; 
                border-radius: 15px; 
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            }
            .btn { 
                background: #3498db; 
                color: white; 
                padding: 12px 24px; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer;
                margin: 5px;
                text-decoration: none;
                display: inline-block;
            }
            .btn:hover { background: #2980b9; }
            .status-normal { border-left: 5px solid #27ae60; }
            .status-medium { border-left: 5px solid #f39c12; }
            .status-high { border-left: 5px solid #e74c3c; }
            .status-critical { border-left: 5px solid #8e44ad; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>PetroSentry - AI-Powered Oil Spill Detection System</h1>
                <p>Dashboard - Real Time</p>
                <button class="btn" onclick="location.reload()">Refresh</button>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{{ stats.total_readings_today }}</div>
                    <div class="stat-label">Readings Last Hour</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ stats.active_alerts }}</div>
                    <div class="stat-label">Active Alerts</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ stats.devices_online }}</div>
                    <div class="stat-label">Devices Online</div>
                </div>
            </div>
            
            <div class="cards">
                <div class="card">
                    <h3>Recent Readings</h3>
                    <div id="readings-container">
                        <p>Loading data...</p>
                    </div>
                </div>
                
                <div class="card">
                    <h3>Recent Alerts</h3>
                    <div id="alerts-container">
                        <p>Loading alerts...</p>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            async function loadReadings() {
                try {
                    const response = await fetch('/api/readings?hours=2');
                    const data = await response.json();
                    
                    const container = document.getElementById('readings-container');
                    container.innerHTML = '';
                    
                    if (data.readings.length === 0) {
                        container.innerHTML = '<p>No recent readings</p>';
                        return;
                    }
                    
                    data.readings.slice(0, 5).forEach(reading => {
                        const div = document.createElement('div');
                        div.className = `status-${reading.threat_level.toLowerCase()}`;
                        div.style.padding = '10px';
                        div.style.marginBottom = '8px';
                        div.style.borderRadius = '5px';
                        
                        const date = new Date(reading.timestamp * 1000);
                        const statusIcon = {
                            'NORMAL': '✅',
                            'MEDIUM': '⚠️',
                            'HIGH': '🔶',
                            'CRITICAL': '🚨'
                        }[reading.threat_level] || '❓';
                        
                        div.innerHTML = `
                            <strong>${statusIcon} ${reading.device_id}</strong><br>
                            <small>${date.toLocaleTimeString()}</small><br>
                            pH: ${reading.ph} | O₂: ${reading.dissolved_oxygen} mg/L<br>
                            HC: ${reading.hydrocarbons} ppm | Battery: ${reading.battery_level}%
                        `;
                        
                        container.appendChild(div);
                    });
                    
                } catch (error) {
                    console.error('Error loading readings:', error);
                    //Showing any errors.
                    document.getElementById('readings-container').innerHTML = '<p>❌ Error loading data</p>';
                }
            }
            
            async function loadAlerts() {
                try {
                    const response = await fetch('/api/alerts?hours=24');
                    const data = await response.json();
                    
                    const container = document.getElementById('alerts-container');
                    container.innerHTML = '';
                    
                    if (data.alerts.length === 0) {
                        container.innerHTML = '<p>No active alerts :))</p>';
                        return;
                    }
                    
                    data.alerts.slice(0, 5).forEach(alert => {
                        const div = document.createElement('div');
                        div.style.padding = '8px';
                        div.style.marginBottom = '5px';
                        div.style.backgroundColor = alert.threat_level === 'CRITICAL' ? '#fee' : '#fef8e7';
                        div.style.borderRadius = '4px';
                        //Showing the threat level
                        const icon = alert.threat_level === 'CRITICAL' ? '🚨' : '⚠️';
                        
                        div.innerHTML = `
                            ${icon} <strong>${alert.device_id}</strong> - ${alert.threat_level}<br>
                            <small>${alert.message}</small>
                        `;
                        
                        container.appendChild(div);
                    });
                    
                } catch (error) {
                    console.error('Error loading alerts:', error);
                    document.getElementById('alerts-container').innerHTML = '<p>Error loading alerts! Try refreshing... </p>';
                }
            }
            
            // Load data on start
            loadReadings();
            loadAlerts();
            
            // Update every 30 seconds
            setInterval(() => {
                loadReadings();
                loadAlerts();
            }, 30000);
        </script>
    </body>
</html>
'''