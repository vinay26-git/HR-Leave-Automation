document.addEventListener('DOMContentLoaded', () => {
    const username = sessionStorage.getItem('username');
    const userRole = sessionStorage.getItem('userRole');
    
    if (!userRole) {
        window.location.href = 'login.html';
        return;
    }

    const usernameDisplay = document.getElementById('username-display');
    const dashboardGrid = document.getElementById('dashboard-grid');
    const logoutLink = document.getElementById('logout-link');

    usernameDisplay.textContent = username;
    
    const card_approvals = `
        <a href="approvals.html" class="dashboard-link">
            <div class="dashboard-card">
                <h3>📧 Daily Approvals</h3>
                <p>Process incoming leave requests from employee emails.</p>
            </div>
        </a>`;

    const card_summary = `
        <a href="summary.html" class="dashboard-link">
            <div class="dashboard-card">
                <h3>🗓️ Monthly Summary</h3>
                <p>Generate and send monthly leave summaries to all employees.</p>
            </div>
        </a>`;
        
    const card_logs = `
        <a href="logs.html" class="dashboard-link">
            <div class="dashboard-card">
                <h3>📜 View Login History</h3>
                <p>See a record of all successful user logins.</p>
            </div>
        </a>`;
        
    const card_lookup = `
        <a href="lookup.html" class="dashboard-link">
            <div class="dashboard-card">
                <h3>🔍 Employee Lookup</h3>
                <p>Quickly find an employee's current leave balance.</p>
            </div>
        </a>`;

    dashboardGrid.innerHTML = '';
    
    if (userRole === 'admin') {
        dashboardGrid.innerHTML = card_approvals + card_summary + card_logs + card_lookup;
    } else if (userRole === 'employee') {
        dashboardGrid.innerHTML = card_lookup;
    }
    
    logoutLink.addEventListener('click', (event) => {
        event.preventDefault();
        sessionStorage.removeItem('username');
        sessionStorage.removeItem('userRole');
        window.location.href = 'login.html';
    });
});