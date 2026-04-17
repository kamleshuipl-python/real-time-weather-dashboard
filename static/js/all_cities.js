document.addEventListener('DOMContentLoaded', () => {
    const refreshButton = document.getElementById('refresh-all-cities');
    const message = document.getElementById('all-cities-message');
    const tbody = document.getElementById('all-cities-body');

    if (!refreshButton || !message || !tbody) {
        return;
    }

    function setMessage(text, isError = false) {
        message.textContent = text;
        message.classList.toggle('error', isError);
    }

    function renderRows(rows) {
        if (!rows.length) {
            tbody.innerHTML = '<tr><td colspan="6">No city data available right now.</td></tr>';
            return;
        }

        tbody.innerHTML = rows.map((row) => `
            <tr>
                <td>${row.city}</td>
                <td>${row.temperature ?? '-'}</td>
                <td>${row.humidity ?? '-'}</td>
                <td>${row.wind ?? '-'}</td>
                <td>${row.timestamp ?? '-'}</td>
                <td>${row.error ?? 'Live'}</td>
            </tr>
        `).join('');
    }

    async function loadAllCities(refresh = true) {
        setMessage(refresh ? 'Refreshing all city weather data...' : 'Loading city weather data...');
        try {
            const response = await fetch(`/api/all-cities?refresh=${refresh ? '1' : '0'}&source=all`);
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Failed to load city weather data');
            }

            renderRows(data.cities || []);
            setMessage(`Showing ${data.cities.length} cities (${data.source || 'live data'}).`);
        } catch (error) {
            setMessage(error.message, true);
        }
    }

    refreshButton.addEventListener('click', () => loadAllCities(true));
    loadAllCities(true);
});
