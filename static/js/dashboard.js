document.addEventListener('DOMContentLoaded', () => {
    const citySelect = document.getElementById('city-select');
    const limitSelect = document.getElementById('limit-select');
    const refreshButton = document.getElementById('refresh-dashboard');
    const message = document.getElementById('dashboard-message');
    const avgTemp = document.getElementById('avg-temp');
    const avgHumidity = document.getElementById('avg-humidity');
    const avgWind = document.getElementById('avg-wind');

    if (!citySelect || !limitSelect || !refreshButton) {
        return;
    }

    const charts = {};

    function average(values) {
        if (!values.length) return 0;
        const total = values.reduce((sum, value) => sum + value, 0);
        return total / values.length;
    }

    function setMessage(text, isError = false) {
        message.textContent = text;
        message.classList.toggle('error', isError);
    }

    function updateKpis(data) {
        avgTemp.textContent = `${average(data.temperature).toFixed(1)} °C`;
        avgHumidity.textContent = `${average(data.humidity).toFixed(1)} %`;
        avgWind.textContent = `${average(data.wind).toFixed(1)} m/s`;
    }

    function buildOrUpdateChart(chartKey, canvasId, label, labels, values, color) {
        const chartData = {
            labels,
            datasets: [{
                label,
                data: values,
                borderColor: color,
                backgroundColor: `${color}33`,
                tension: 0.25,
                fill: true
            }]
        };

        if (charts[chartKey]) {
            charts[chartKey].data = chartData;
            charts[chartKey].update();
            return;
        }

        const context = document.getElementById(canvasId).getContext('2d');
        charts[chartKey] = new Chart(context, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: false } }
            }
        });
    }

    async function loadDashboard() {
        const city = citySelect.value.trim();
        const limit = limitSelect.value;
        const query = new URLSearchParams({ limit });
        if (city) query.append('city', city);

        setMessage('Loading chart data...');

        try {
            const response = await fetch(`/api/history?${query.toString()}`);
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Failed to load chart data');
            }

            buildOrUpdateChart('temperature', 'temperature-chart', 'Temperature (°C)', data.labels, data.temperature, '#ff6384');
            buildOrUpdateChart('humidity', 'humidity-chart', 'Humidity (%)', data.labels, data.humidity, '#36a2eb');
            buildOrUpdateChart('wind', 'wind-chart', 'Wind (m/s)', data.labels, data.wind, '#4bc0c0');
            updateKpis(data);
            setMessage(`Showing ${data.labels.length} records for ${data.city}.`);
        } catch (error) {
            setMessage(error.message, true);
        }
    }

    refreshButton.addEventListener('click', loadDashboard);
    citySelect.addEventListener('change', loadDashboard);
    limitSelect.addEventListener('change', loadDashboard);
    loadDashboard();
});
