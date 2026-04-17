document.addEventListener('DOMContentLoaded', () => {
    const citySelect = document.getElementById('city-select');
    const limitSelect = document.getElementById('limit-select');
    const refreshButton = document.getElementById('refresh-chart');
    const message = document.getElementById('chart-message');
    const chartConfig = document.getElementById('chart-config');
    const canvas = document.getElementById('metric-chart');

    if (!citySelect || !limitSelect || !refreshButton || !chartConfig || !canvas) {
        return;
    }

    const metric = chartConfig.dataset.metric;
    const label = chartConfig.dataset.label;
    const color = chartConfig.dataset.color;
    let chart = null;

    function setMessage(text, isError = false) {
        message.textContent = text;
        message.classList.toggle('error', isError);
    }

    function renderChart(labels, values) {
        const data = {
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

        if (chart) {
            chart.data = data;
            chart.update();
            return;
        }

        chart = new Chart(canvas.getContext('2d'), {
            type: 'line',
            data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: false } }
            }
        });
    }

    async function loadChartData() {
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

            renderChart(data.labels, data[metric]);
            setMessage(`Showing ${data.labels.length} records for ${data.city}.`);
        } catch (error) {
            setMessage(error.message, true);
        }
    }

    refreshButton.addEventListener('click', loadChartData);
    citySelect.addEventListener('change', loadChartData);
    limitSelect.addEventListener('change', loadChartData);
    loadChartData();
});
