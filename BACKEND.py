from flask import Flask, jsonify, send_from_directory, request
import random
import requests
from datetime import datetime

app = Flask(__name__)

# --- COMPLETE DATASET FOR ALL TABS ---
DATASET = {
    # Data for the initial status bar and HUD
    "stats": {
        "activeProjects": 247,
        "totalCapacity": "1.2 GW",
        "efficiency": "94%",
        "costReduction": "-23%"
    },

    # Data for the Layers tab and map population
    "layers": {
        "infrastructure": [
            {"lat": 40.7128, "lng": -74.0060, "name": "Manhattan H2 Hub", "type": "production", "capacity": "75 MW", "status": "operational"},
            {"lat": 34.0522, "lng": -118.2437, "name": "LA Port Storage", "type": "storage", "capacity": "2000 kg", "status": "construction"},
            {"lat": 41.8781, "lng": -87.6298, "name": "Chicago Pipeline", "type": "pipeline", "length": "200 km", "status": "operational"},
            {"lat": 29.7604, "lng": -95.3698, "name": "Houston Mega Plant", "type": "production", "capacity": "150 MW", "status": "operational"},
            {"lat": 39.9526, "lng": -75.1652, "name": "Philadelphia Storage", "type": "storage", "capacity": "1500 kg", "status": "planned"},
            {"lat": 33.4484, "lng": -112.0740, "name": "Phoenix Solar H2", "type": "production", "capacity": "100 MW", "status": "construction"},
            {"lat": 47.6062, "lng": -122.3321, "name": "Seattle Port Hub", "type": "storage", "capacity": "3000 kg", "status": "operational"},
            {"lat": 39.7392, "lng": -104.9903, "name": "Denver Distribution", "type": "pipeline", "length": "150 km", "status": "planned"}
        ],
        "renewables": {
            "solar": [
                [40.7128, -74.0060, 0.7], [34.0522, -118.2437, 0.95], [29.7604, -95.3698, 0.88],
                [33.4484, -112.0740, 0.98], [25.7617, -80.1918, 0.92], [39.7392, -104.9903, 0.85],
                [36.1627, -115.1627, 0.96], [32.7767, -96.7970, 0.82], [30.2672, -97.7431, 0.86]
            ],
            "wind": [
                [41.8781, -87.6298, 0.82], [39.9526, -75.1652, 0.75], [47.6062, -122.3321, 0.88],
                [44.9778, -93.2650, 0.92], [39.1612, -75.5264, 0.78], [42.3601, -71.0589, 0.72],
                [41.2524, -95.9980, 0.89], [40.2731, -86.1349, 0.76], [39.7391, -104.9847, 0.81]
            ]
        },
        "demandCenters": [
            {"lat": 40.7128, "lng": -74.0060, "name": "NYC Industrial Complex", "demand": 92, "type": "industrial"},
            {"lat": 34.0522, "lng": -118.2437, "name": "LA Port Authority", "demand": 88, "type": "transport"},
            {"lat": 41.8781, "lng": -87.6298, "name": "Chicago Manufacturing", "demand": 85, "type": "industrial"},
            {"lat": 29.7604, "lng": -95.3698, "name": "Houston Energy District", "demand": 98, "type": "industrial"},
            {"lat": 47.6062, "lng": -122.3321, "name": "Seattle Maritime", "demand": 76, "type": "transport"},
            {"lat": 33.4484, "lng": -112.0740, "name": "Phoenix Tech Hub", "demand": 68, "type": "industrial"},
            {"lat": 39.7392, "lng": -104.9903, "name": "Denver Logistics", "demand": 72, "type": "transport"}
        ],
        "regulatoryZones": [
            {"lat": 40.7829, "lng": -73.9654, "bounds": [[40.7629, -73.9854], [40.8029, -73.9454]], "name": "Central Park Protected"},
            {"lat": 37.8044, "lng": -122.2711, "bounds": [[37.7844, -122.2911], [37.8244, -122.2511]], "name": "Bay Area Marine Sanctuary"},
            {"lat": 38.9072, "lng": -77.0369, "bounds": [[38.8872, -77.0569], [38.9272, -77.0169]], "name": "DC Federal Zone"}
        ]
    },
    "search": {
        "recent": [
            {"name": "New York City", "lat": 40.7128, "lng": -74.0060, "subtitle": "Manhattan Financial District", "icon": "🏙️"},
            {"name": "Los Angeles", "lat": 34.0522, "lng": -118.2437, "subtitle": "Port of Long Beach", "icon": "🌴"},
            {"name": "Houston", "lat": 29.7604, "lng": -95.3698, "subtitle": "Energy Corridor", "icon": "🛢️"}
        ],
        "strategicHubs": [
            {"name": "Arizona Solar Belt", "lat": 33.4484, "lng": -112.0740, "subtitle": "Peak solar potential • 28 active projects", "icon": "☀️"},
            {"name": "Great Lakes Wind Hub", "lat": 41.8781, "lng": -87.6298, "subtitle": "Offshore wind corridor • 15 facilities", "icon": "💨"},
            {"name": "Pacific Northwest Port", "lat": 47.6062, "lng": -122.3321, "subtitle": "Green shipping gateway • Export ready", "icon": "🚢"}
        ],
        "database": []
    },
    "recommendations": [
        {
            "name": "Texas Gulf Coast Mega Hub", "lat": 29.3013, "lng": -94.7977,
            "description": "AI-identified optimal location combining exceptional solar resources, industrial demand proximity, and existing infrastructure",
            "metrics": {"capacity": "200 MW", "proximity": "1.2 km", "investment": "$120M", "score": "97%", "roi": "18.5%", "risk": "Low"}
        },
        {
            "name": "California Central Valley Solar", "lat": 36.7783, "lng": -119.4179,
            "description": "Premium solar irradiance zone with excellent grid connectivity and transport infrastructure access",
            "metrics": {"capacity": "150 MW", "proximity": "3.8 km", "investment": "$95M", "score": "94%", "roi": "16.2%", "risk": "Low"}
        },
        {
            "name": "Midwest Wind Corridor Hub", "lat": 41.5868, "lng": -93.6250,
            "description": "Exceptional wind resources with established grid infrastructure and favorable regulatory environment",
            "metrics": {"capacity": "180 MW", "proximity": "2.1 km", "investment": "$108M", "score": "91%", "roi": "15.8%", "risk": "Medium"}
        }
    ]
}

# Populate the search database with data from layers
DATASET['search']['database'] = [
    {"name": item['name'], "type": "infrastructure", "lat": item['lat'], "lng": item['lng'],
     "subtitle": f"{item['type']} • {item.get('capacity', item.get('length', 'N/A'))} • {item['status']}",
     "icon": "🏭" if item['type'] == "production" else "📦" if item['type'] == "storage" else "🔗"
    } for item in DATASET['layers']['infrastructure']
]
# --- END DATASET ---

# --- API ROUTES ---

@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'FRONTEND.html')

@app.route('/api/initial-data')
def get_initial_data():
    return jsonify(DATASET)

@app.route('/api/search', methods=['POST'])
def search_locations():
    query = request.json.get('query', '').lower()
    
    # Simple search logic
    results = [
        item for item in DATASET['search']['database']
        if query in item['name'].lower() or query in item['subtitle'].lower()
    ]
    
    # Add coordinate search
    import re
    coord_match = re.match(r'^(-?\d+\.?\d*),\s*(-?\d+\.?\d*)$', query)
    if coord_match:
        lat, lng = float(coord_match[1]), float(coord_match[2])
        results.insert(0, {
            "name": f"Coordinates: {lat}, {lng}",
            "type": "coordinates",
            "lat": lat,
            "lng": lng,
            "subtitle": "Custom location for analysis",
            "icon": "📍"
        })
    
    return jsonify(results[:6])

@app.route('/api/run-analysis', methods=['POST'])
def run_ai_analysis():
    data = request.json
    lat = float(data.get('lat'))
    lng = float(data.get('lng'))
    renewable_weight = float(data.get('renewableWeight'))
    demand_weight = float(data.get('demandWeight'))
    cost_threshold = float(data.get('costThreshold'))
    risk_level = data.get('riskLevel')
    
    print(f"Running AI analysis for LAT: {lat}, LNG: {lng}")
    print(f"- Renewable Weight: {renewable_weight}%")
    
    # --- Integration with NASA POWER API ---
    try:
        start_date = datetime.now().strftime("%Y%m%d")
        end_date = start_date
        
        api_url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=ALLSKY_SFC_SW_DWN&community=RE&longitude={lng}&latitude={lat}&start={start_date}&end={end_date}&format=JSON"
        response = requests.get(api_url)
        response.raise_for_status()
        solar_data = response.json()
        
        solar_value = solar_data['properties']['parameter']['ALLSKY_SFC_SW_DWN'][start_date]
        
        solar_score = (solar_value / 8000) * 100
        final_score = (solar_score * (renewable_weight / 100) + random.randint(80, 95) * (demand_weight / 100)) / 2
        
        new_recommendation = {
            "name": "AI-Generated Optimal Site",
            "lat": lat, "lng": lng,
            "description": f"Optimized site based on real-time solar data (All Sky Irradiance: {solar_value:.2f} Wh/m^2/day).",
            "metrics": {
                "capacity": "Dynamic",
                "proximity": "N/A",
                "investment": "$75M",
                "score": f"{final_score:.1f}%",
                "roi": "15.0%",
                "risk": "Low" if final_score > 90 else "Medium"
            }
        }
        
        results = [new_recommendation] + DATASET['recommendations']
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling NASA API: {e}")
        results = DATASET['recommendations']

    random.shuffle(results)
    
    return jsonify({"recommendations": results})

if __name__ == '__main__':
    app.run(debug=True)