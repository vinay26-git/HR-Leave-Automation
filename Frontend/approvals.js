document.addEventListener('DOMContentLoaded', () => {
    const pendingView = document.getElementById('pending-request-view');
    const noRequestsView = document.getElementById('no-requests-view');
    const successView = document.getElementById('success-view');
    const loadingView = document.getElementById('loading-view');
    const errorView = document.getElementById('error-view');
    const approveBtn = document.getElementById('approve-btn');
    const rejectBtn = document.getElementById('reject-btn');
    const nextRequestBtn = document.getElementById('next-request-btn');
    // MODIFICATION: Get the new admin note textarea
    const adminNoteTextarea = document.getElementById('admin-note');
    const backendUrl = 'http://127.0.0.1:5000';
    let currentRequestData = null;

    function showView(viewToShow) {
        [pendingView, noRequestsView, successView, loadingView, errorView].forEach(view => {
            if (view) view.style.display = 'none';
        });
        if (viewToShow) viewToShow.style.display = 'block';
    }

    async function fetchPendingRequest() {
        showView(loadingView);
        try {
            const response = await fetch(`${backendUrl}/get-pending-requests`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            if (data.status === 'no_requests') {
                document.getElementById('no-requests-message').textContent = data.message;
                showView(noRequestsView);
            } else if (data.status === 'pending_request') {
                currentRequestData = data.request;
                displayRequest(currentRequestData);
                showView(pendingView);
            }
        } catch (error) {
            console.error("Error fetching request:", error);
            document.getElementById('error-message').textContent = `Failed to connect to the backend. Ensure it's running. Details: ${error.message}`;
            showView(errorView);
        }
    }

    function displayRequest(request) {
        document.getElementById('sender-email').textContent = request.sender_email;
        document.getElementById('employee-name').textContent = request.employee_name;
        document.getElementById('request-subject').textContent = request.subject;
        
        const detailsHtml = request.parsed_details.map(detail => 
            `<li>${detail.date} - <strong>${detail.type.replace('_', ' ')}</strong></li>`
        ).join('');
        document.getElementById('request-details-list').innerHTML = detailsHtml;

        let totalsText = [];
        if (request.total_leave_days > 0) totalsText.push(`${request.total_leave_days} Leave Day(s)`);
        if (request.total_wfh_days > 0) totalsText.push(`${request.total_wfh_days} WFH Day(s)`);
        document.getElementById('request-totals').textContent = totalsText.join(' & ');

        // MODIFICATION: Clear the note textarea for the new request
        adminNoteTextarea.value = '';
    }

    async function processDecision(decision) {
        showView(loadingView);
        try {
            const userInfo = {
                username: sessionStorage.getItem('username'),
                role: sessionStorage.getItem('userRole')
            };
            
            // MODIFICATION: Get the note from the textarea
            const adminNote = adminNoteTextarea.value.trim();

            const response = await fetch(`${backendUrl}/process-decision`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                // MODIFICATION: Send the admin_note along with other data
                body: JSON.stringify({ 
                    decision: decision, 
                    request_data: currentRequestData,
                    admin_note: adminNote, // Sending the note
                    userInfo: userInfo 
                })
            });
            const result = await response.json();
            if (response.ok && result.status === 'success') {
                const message = (decision === 'approve') 
                    ? `✅ Request for ${currentRequestData.employee_name} approved successfully.`
                    : `❌ Request for ${currentRequestData.employee_name} has been rejected and a reply was sent.`;
                document.getElementById('success-message').textContent = message;
                showView(successView);
            } else {
                throw new Error(result.message || 'An unknown error occurred.');
            }
        } catch (error) {
            console.error("Error processing decision:", error);
            document.getElementById('error-message').textContent = `An error occurred: ${error.message}`;
            showView(errorView);
        }
    }

    approveBtn.addEventListener('click', () => processDecision('approve'));
    rejectBtn.addEventListener('click', () => processDecision('reject'));
    nextRequestBtn.addEventListener('click', fetchPendingRequest);
    fetchPendingRequest();
});