from flask import Blueprint, render_template, request, jsonify, current_app
from app import db
from app.models import City, Weather
import requests
from sqlalchemy import desc

main = Blueprint('main', __name__)
DEFAULT_REALTIME_CITIES = [
    'Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', 'Ahmedabad',
    'Chennai', 'Kolkata', 'Surat', 'Pune', 'Jaipur',
    'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane',
    'Bhopal', 'Visakhapatnam', 'Pimpri-Chinchwad', 'Patna', 'Vadodara',
    'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik', 'Faridabad',
    'Meerut', 'Rajkot', 'Kalyan', 'Vasai', 'Varanasi',
    'Srinagar', 'Aurangabad', 'Dhanbad', 'Amritsar', 'Navi Mumbai',
    'Allahabad', 'Howrah', 'Ranchi', 'Gwalior', 'Jabalpur',
    'Coimbatore', 'Vijayawada', 'Jodhpur', 'Madurai', 'Raipur',
    'Kota', 'Guwahati', 'Chandigarh', 'Solapur', 'Hubballi',
    'Tiruchirappalli', 'Bareilly', 'Mysuru', 'Tiruppur', 'Gurgaon',
    'Aligarh', 'Jalandhar', 'Bhubaneswar', 'Salem', 'Warangal',
    'Mira-Bhayandar', 'Thiruvananthapuram', 'Bhiwandi', 'Saharanpur', 'Gorakhpur',
    'Guntur', 'Bikaner', 'Amravati', 'Noida', 'Jamshedpur',
    'Bhilai', 'Cuttack', 'Firozabad', 'Kochi', 'Nellore',
    'Bhavnagar', 'Dehradun', 'Durgapur', 'Asansol', 'Rourkela',
    'Nanded', 'Kolhapur', 'Ajmer', 'Akola', 'Gulbarga',
    'Jamnagar', 'Ujjain', 'Loni', 'Siliguri', 'Jhansi',
    'Ulhasnagar', 'Jammu', 'Sangli', 'Mangalore', 'Erode',
    'Belgaum', 'Ambattur', 'Tirunelveli', 'Malegaon', 'Gaya'
]


@main.route('/favicon.ico')
def favicon():
    return '', 204


def fetch_live_weather(city_name):
    api_key = current_app.config.get('OPENWEATHER_API_KEY')
    base_url = current_app.config.get('OPENWEATHER_BASE_URL')

    try:
        if api_key:
            response = requests.get(
                base_url,
                params={'q': city_name, 'units': 'metric', 'appid': api_key},
                timeout=10
            )
            if response.status_code != 200:
                return None, 'City not found or API error'

            data = response.json()
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed']
            }, None

        geocode = requests.get(
            'https://geocoding-api.open-meteo.com/v1/search',
            params={'name': city_name, 'count': 1, 'language': 'en', 'format': 'json'},
            timeout=10
        )
        geocode_data = geocode.json()
        results = geocode_data.get('results', [])
        if not results:
            return None, 'City not found'

        lat = results[0]['latitude']
        lon = results[0]['longitude']
        weather_response = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params={'latitude': lat, 'longitude': lon, 'current': 'temperature_2m,relative_humidity_2m,wind_speed_10m'},
            timeout=10
        )
        weather_data = weather_response.json().get('current')
        if not weather_data:
            return None, 'Weather service unavailable'

        return {
            'temperature': weather_data['temperature_2m'],
            'humidity': weather_data['relative_humidity_2m'],
            'wind': weather_data['wind_speed_10m']
        }, None
    except requests.RequestException:
        return None, 'Failed to reach weather service'


def save_weather_for_city(city_name, weather_data):
    city = City.query.filter_by(name=city_name).first()
    if not city:
        city = City(name=city_name)
        db.session.add(city)
        db.session.commit()

    weather = Weather(
        city_id=city.id,
        temperature=weather_data['temperature'],
        humidity=weather_data['humidity'],
        wind=weather_data['wind']
    )
    db.session.add(weather)
    db.session.commit()
    return city, weather

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/dashboard')
def dashboard():
    cities = City.query.order_by(City.name.asc()).all()
    return render_template('dashboard.html', cities=cities)

@main.route('/all-cities')
def all_cities():
    return render_template('all_cities.html')

@main.route('/dashboard/temperature')
def temperature_dashboard():
    cities = City.query.order_by(City.name.asc()).all()
    return render_template(
        'chart_page.html',
        cities=cities,
        chart_title='Temperature Trend',
        chart_metric='temperature',
        chart_label='Temperature (°C)',
        chart_color='#ff6384'
    )

@main.route('/dashboard/humidity')
def humidity_dashboard():
    cities = City.query.order_by(City.name.asc()).all()
    return render_template(
        'chart_page.html',
        cities=cities,
        chart_title='Humidity Trend',
        chart_metric='humidity',
        chart_label='Humidity (%)',
        chart_color='#36a2eb'
    )

@main.route('/dashboard/wind')
def wind_dashboard():
    cities = City.query.order_by(City.name.asc()).all()
    return render_template(
        'chart_page.html',
        cities=cities,
        chart_title='Wind Speed Trend',
        chart_metric='wind',
        chart_label='Wind Speed (m/s)',
        chart_color='#4bc0c0'
    )

@main.route('/api/history')
def get_history():
    city_name = request.args.get('city', '').strip()
    limit = request.args.get('limit', type=int) or 20
    limit = max(5, min(limit, 100))

    query = Weather.query.join(City).order_by(desc(Weather.timestamp))
    if city_name:
        query = query.filter(City.name.ilike(city_name))

    records = query.limit(limit).all()
    if not records:
        return jsonify({'error': 'No weather history found'}), 404

    ordered = list(reversed(records))
    return jsonify({
        'labels': [w.timestamp.strftime('%Y-%m-%d %H:%M') for w in ordered],
        'temperature': [w.temperature for w in ordered],
        'humidity': [w.humidity for w in ordered],
        'wind': [w.wind for w in ordered],
        'city': city_name or 'All Cities'
    })

@main.route('/api/all-cities')
def get_all_cities_weather():
    refresh = request.args.get('refresh', '1') == '1'
    source = request.args.get('source', 'all').strip().lower()
    include_defaults = source in ('all', 'default', '')

    saved_cities = City.query.order_by(City.name.asc()).all()
    saved_city_map = {city.name.lower(): city for city in saved_cities}
    city_names = {city.name for city in saved_cities}
    if include_defaults:
        city_names.update(DEFAULT_REALTIME_CITIES)

    if not city_names:
        return jsonify({'cities': [], 'message': 'No cities found'}), 200

    rows = []
    for city_name in sorted(city_names):
        city = saved_city_map.get(city_name.lower())
        latest_weather = None
        if city:
            latest_weather = Weather.query.filter_by(city_id=city.id).order_by(desc(Weather.timestamp)).first()

        if refresh:
            weather_data, error = fetch_live_weather(city_name)
            if weather_data:
                city, latest_weather = save_weather_for_city(city_name, weather_data)
            else:
                rows.append({
                    'city': city_name,
                    'error': error
                })
                continue

        if not latest_weather:
            rows.append({
                'city': city_name,
                'error': 'Weather data not available'
            })
            continue

        rows.append({
            'city': city.name,
            'temperature': latest_weather.temperature,
            'humidity': latest_weather.humidity,
            'wind': latest_weather.wind,
            'timestamp': latest_weather.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify({
        'cities': rows,
        'total': len(rows),
        'source': 'saved + india cities' if include_defaults else 'saved cities'
    })

@main.route('/api/weather')
def get_weather():
    city_name = request.args.get('city')
    if not city_name:
        return jsonify({'error': 'No city provided'}), 400
    city_name = city_name.strip()
    if not city_name:
        return jsonify({'error': 'No city provided'}), 400

    weather_data, error = fetch_live_weather(city_name)
    if error:
        status_code = 404 if error in ('City not found', 'City not found or API error') else 502
        return jsonify({'error': error}), status_code

    _, weather = save_weather_for_city(city_name, weather_data)

    return jsonify({
        'temperature': weather.temperature,
        'humidity': weather.humidity,
        'wind': weather.wind
    })