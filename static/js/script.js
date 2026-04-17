document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('weather-form');
    const resultDiv = document.getElementById('weather-result');
    if (!form || !resultDiv) {
        return;
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const city = form.elements['city'].value.trim();
        if (!city) return;
        fetch(`/api/weather?city=${city}`)
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
                } else {
                    resultDiv.innerHTML = `
                        <h3>Weather in ${city}</h3>
                        <p>Temperature: ${data.temperature} &deg;C</p>
                        <p>Humidity: ${data.humidity} %</p>
                        <p>Wind: ${data.wind} m/s</p>
                    `;
                }
            })
            .catch(err => {
                resultDiv.innerHTML = '<p>Error fetching data</p>';
            });
    });
});