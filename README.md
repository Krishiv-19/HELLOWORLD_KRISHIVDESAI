HydroGen Pro - Advanced H2 Infrastructure

Overview
HydroGen Pro is a powerful, interactive GIS-based platform designed to accelerate the strategic planning and development of the green hydrogen ecosystem. It serves as a data-driven decision support tool for urban planners, energy companies, and policy analysts.

The application’s core value is its ability to integrate and visualize complex, multi-layered data—such as existing infrastructure, renewable energy resources, and market demand—on a single map. It features a sophisticated AI model that performs multi-criteria optimization to identify the single most optimal site for new projects, ensuring capital is directed to the most impactful and high-yield locations.

Key Features
Secure Login & Authentication: A secure login system using a Python backend with werkzeug for password hashing and Flask sessions for state management.
Interactive GIS Mapping: A dynamic map interface built with Leaflet.js that serves as the central visualization hub for all data layers.
Multi-Criteria AI Analysis: The platform's most powerful feature, a multi-criteria optimization model that analyzes a location based on user-defined weights for renewable energy potential, demand proximity, cost, and risk to recommend the best-fit site.
Live Data Integration: The backend seamlessly integrates with external APIs, such as the NASA POWER Project API, to pull real-time solar data for dynamic and accurate analysis.
Dynamic Data Layers: Users can toggle various data layers on and off, including existing infrastructure, renewable energy heatmaps, demand centers, and regulatory zones.
Search & Navigation: A real-time search functionality that allows users to find locations and assets, with dynamic results displayed instantly.
Data Management: A dedicated settings panel for managing data, including options to refresh data from live APIs and export GeoJSON data for external use.

Technology Stack
Frontend:

HTML5/CSS3: Structure, styling, and animations.
JavaScript: Core logic for client-side interactivity.
Leaflet.js: Open-source library for interactive maps.
Leaflet.heat: Plugin for visualizing heatmaps.
Font Awesome: Icon library.

Backend:
Python 3.x: Server-side logic.
Flask: Web framework for creating API endpoints.
Requests: Library for making HTTP requests to external APIs.
Werkzeug: Security library for password hashing.
Numpy & Scipy: Libraries for numerical operations and optimization modeling.

Installation and Setup
To get the HydroGen Pro application up and running, follow these steps:
Prerequisites: Ensure you have Python 3.x and pip installed on your system.
File Setup:
Place both FRONTEND.html and app.py in the same folder.
Install Dependencies:
Open your terminal or command prompt.
Navigate to the directory containing your project files.
Install the required Python libraries with the following command:
Bash
pip install Flask werkzeug requests numpy scipy
Set Your API Key:
Open app.py in a text editor.
Find the NREL_API_KEY variable and replace 'YOUR_NREL_API_KEY' with your actual, unique API key from the NREL Developer Network.
Run the Application:
In your terminal, execute the Python script:
Bash
python app.py
The server will start running. Open your web browser and go to:
http://127.0.0.1:5000

Usage Guide
Log In: Use the mock credentials admin / password123 to access the application.
Explore Data: Use the "Layers" tab to toggle data layers on and off.
Search: Use the "Search" tab to find locations or assets by name.
Run AI Analysis: Go to the "AI" tab, adjust the sliders to define your priorities, and click "Run AI Analysis" to get a single, optimized site recommendation.
Data Management: Use the "Settings" tab to refresh your data or export the current map layers.
