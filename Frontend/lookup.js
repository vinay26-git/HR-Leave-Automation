document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('results-container');
    const heading = document.getElementById('lookup-heading');
    const instruction = document.getElementById('lookup-instruction');
    
    const historySection = document.getElementById('history-section');
    const historyTableBody = document.getElementById('history-table-body');
    const historyLoader = document.getElementById('history-loader');

    const backendUrl = 'http://127.0.0.1:5000';

    const loggedInUser = sessionStorage.getItem('username');
    const userRole = sessionStorage.getItem('userRole');

    if (!loggedInUser || !userRole) {
        window.location.href = 'login.html';
        return;
    }

    if (userRole === 'employee') {
        heading.textContent = 'My Leave Summary';
        instruction.style.display = 'none';
        searchForm.remove();
        fetchData(loggedInUser);
    } else {
        resultsContainer.innerHTML = '<div class="status-message info">Type a name above and click search to see results.</div>';
        searchForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const searchTerm = searchInput.value.trim();
            if (searchTerm) {
                fetchData(searchTerm);
            }
        });
    }

    async function fetchData(searchTerm) {
        resultsContainer.innerHTML = '<div class="loader"></div>';
        try {
            const url = `${backendUrl}/search-employee?name=${encodeURIComponent(searchTerm)}&role=${encodeURIComponent(userRole)}&user=${encodeURIComponent(loggedInUser)}`;
            const response = await fetch(url);
            const results = await response.json();
            displayResults(results);
        } catch (error) {
            console.error('Search error:', error);
            resultsContainer.innerHTML = '<div class="status-message" style="background-color: #f8d7da; color: #721c24;">Error connecting to the server.</div>';
        }
    }

    function displayResults(employees) {
        resultsContainer.innerHTML = '';
        if (!employees || employees.length === 0) {
            resultsContainer.innerHTML = '<div class="status-message info">No employee data found.</div>';
            return;
        }

        employees.forEach(employee => {
            const card = document.createElement('div');
            card.className = 'result-card';
            
            let actionButtons = '';
            if (userRole === 'employee') {
                actionButtons = `
                    <div class="button-group" style="margin-top: 2rem; justify-content: space-between;">
                        <button id="view-history-btn" class="btn btn-secondary" style="width: auto;">View Leave History</button>
                        <a href="apply_leave.html" class="btn btn-primary" style="width: auto;">Apply for Leave</a>
                    </div>
                `;
            }

            card.innerHTML = `
                <h3 class="result-card-name">${employee.Name}</h3>
                <p class="result-card-email">${employee.Email}</p>
                <div class="result-card-stats">
                    <div class="stat-item"><span>Total Leaves</span><strong>${employee.Total || 0}</strong></div>
                    <div class="stat-item"><span>Used</span><strong>${employee.Used || 0}</strong></div>
                    <div class="stat-item"><span>Available</span><strong>${employee.Available || 0}</strong></div>
                    <div class="stat-item"><span>WFH</span><strong>${employee.WFH || 0}</strong></div>
                </div>
                ${actionButtons}
            `;
            resultsContainer.appendChild(card);
        });

        const historyBtn = document.getElementById('view-history-btn');
        if (historyBtn) {
            historyBtn.addEventListener('click', toggleHistoryView);
        }
    }

    async function toggleHistoryView() {
        if (historySection.style.display === 'block') {
            historySection.style.display = 'none';
            document.getElementById('view-history-btn').textContent = 'View Leave History';
            return;
        }

        historySection.style.display = 'block';
        historyLoader.style.display = 'block';
        historyTableBody.innerHTML = '';
        document.getElementById('view-history-btn').textContent = 'Loading...';
        document.getElementById('view-history-btn').disabled = true;

        try {
            const url = `${backendUrl}/get-my-leave-history?user=${encodeURIComponent(loggedInUser)}`;
            const response = await fetch(url);
            const historyData = await response.json();

            historyLoader.style.display = 'none';

            if (historyData.length === 0) {
                historyTableBody.innerHTML = '<tr><td colspan="2">No leave history found.</td></tr>';
            } else {
                historyData.forEach(record => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${record.date}</td>
                        <td>${record.type}</td>
                    `;
                    historyTableBody.appendChild(row);
                });
            }
            document.getElementById('view-history-btn').textContent = 'Hide History';
        } catch (error) {
            console.error("Failed to fetch history:", error);
            historyLoader.style.display = 'none';
            historyTableBody.innerHTML = '<tr><td colspan="2">Error loading history.</td></tr>';
        } finally {
            document.getElementById('view-history-btn').disabled = false;
        }
    }
});