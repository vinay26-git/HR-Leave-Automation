document.addEventListener('DOMContentLoaded', async () => {
    const logTableBody = document.getElementById('log-table-body');
    const backendUrl = 'http://127.0.0.1:5000'; // Your Daily Approvals server

    try {
        const response = await fetch(`${backendUrl}/view-logs`);
        const logs = await response.json();

        if (logs.length === 0) {
            logTableBody.innerHTML = '<tr><td colspan="2">No login history found.</td></tr>';
            return;
        }

        // Loop through each log entry and create a table row
        logs.forEach(log => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${log.username}</td>
                <td>${log.login_timestamp}</td>
            `;
            logTableBody.appendChild(row);
        });

    } catch (error) {
        console.error('Failed to fetch logs:', error);
        logTableBody.innerHTML = '<tr><td colspan="2">Error loading log data.</td></tr>';
    }
});