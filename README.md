# Real-Time Weather Dashboard
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/kamleshuipl-python/real-time-weather-dashboard)

This project is a web-based, real-time weather dashboard built using Python and Flask. It allows users to fetch current weather data for any city, view historical weather trends through interactive charts, and see a live overview of weather conditions across multiple cities.

## Features

-   **Live Weather Search:** Get the current temperature, humidity, and wind speed for any city.
-   **Historical Data:** Fetched weather data is automatically saved to a local SQLite database.
-   **Analytics Dashboard:** Visualize historical data for temperature, humidity, and wind speed using line charts powered by Chart.js.
-   **Data Filtering:** Filter historical charts by city and the number of data points to display.
-   **Multi-City View:** A dedicated page to display the latest weather for a comprehensive list of cities, with an option to refresh all data on demand.
-   **Dual API Integration:** Uses the OpenWeatherMap API if a key is provided, otherwise falls back to the free Open-Meteo API for weather data.
-   **Responsive UI:** A clean and modern user interface built with HTML, CSS, and vanilla JavaScript.

## Technology Stack

-   **Backend:** Python, Flask, Flask-SQLAlchemy
-   **Database:** SQLite
-   **Frontend:** HTML, CSS, JavaScript (ES6+), Chart.js
-   **APIs:** OpenWeatherMap, Open-Meteo Geocoding & Weather Forecast

## Installation and Setup

Follow these steps to get the application running on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kamleshuipl-python/real-time-weather-dashboard.git
    cd real-time-weather-dashboard
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Unix/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    -   Create a `.env` file in the root directory by copying the example file:
        ```bash
        cp .env.example .env
        ```
    -   Open the `.env` file and add your OpenWeatherMap API key (this is optional):
        ```
        OPENWEATHER_API_KEY=your_openweathermap_api_key_here
        ```
    > **Note:** If you do not provide an `OPENWEATHER_API_KEY`, the application will automatically use the free Open-Meteo API as a fallback.

5.  **Run the application:**
    ```bash
    python run.py
    ```
    The application will start, create the `weather.db` database file if it doesn't exist, and be accessible at `http://127.0.0.1:5000`.

## Project Structure

```
.
├── app/                  # Main application package
│   ├── __init__.py       # Initializes the Flask app and extensions
│   ├── config.py         # Configuration settings
│   ├── models.py         # SQLAlchemy database models (City, Weather)
│   └── routes.py         # Application routes and API endpoints
├── instance/
│   └── weather.db        # SQLite database file
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates
├── .env.example          # Example environment variable file
├── requirements.txt      # Python dependencies
└── run.py                # Application entry point
```

## Usage Guide

-   **Home Page (`/`):** Use the search bar to get the immediate live weather for any specified city. The data is fetched and displayed on the page, and also saved to the database.

-   **All Cities (`/all-cities`):** View a table showing the latest recorded weather for a default list of Indian cities plus any cities you have previously searched for. Use the "Refresh All Cities" button to fetch new live data for every city in the list.

-   **Dashboard (`/dashboard`):** This page provides navigation to detailed chart views for different weather metrics (Temperature, Humidity, Wind Speed).

-   **Chart Pages (`/dashboard/<metric>`):** These pages display interactive line charts for historical weather data. You can use the dropdowns to filter the data by a specific city (or all cities) and limit the number of records shown.
