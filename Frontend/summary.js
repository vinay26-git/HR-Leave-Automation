// summary.js

document.addEventListener('DOMContentLoaded', () => {
    const initialView = document.getElementById('initial-view');
    const processingView = document.getElementById('processing-view');
    const completionView = document.getElementById('completion-view');
    
    const startButton = document.getElementById('start-summary-btn');
    const completionMessage = document.getElementById('completion-message');

    // Lists for results
    const successList = document.getElementById('success-list');
    const failureListContainer = document.getElementById('failure-list-container');
    const failureList = document.getElementById('failure-list');
    
    const backendUrl = 'http://127.0.0.1:5001';

    function showView(viewToShow) {
        [initialView, processingView, completionView].forEach(view => {
            view.style.display = 'none';
        });
        if (viewToShow) viewToShow.style.display = 'block';
    }

    // NEW function to display the clean summary
    function displaySummaryResults(data) {
        // Clear previous results
        successList.innerHTML = '';
        failureList.innerHTML = '';

        // Populate the list of successful sends
        if (data.sent_to && data.sent_to.length > 0) {
            data.sent_to.forEach(name => {
                const li = document.createElement('li');
                li.textContent = name;
                successList.appendChild(li);
            });
        } else {
            successList.innerHTML = '<li>No summaries were sent successfully.</li>';
        }

        // Populate the list of failed sends, ONLY if there are any
        if (data.failed_to_send && data.failed_to_send.length > 0) {
            failureListContainer.style.display = 'block'; // Show the failure section
            data.failed_to_send.forEach(name => {
                const li = document.createElement('li');
                li.textContent = name;
                failureList.appendChild(li);
            });
        } else {
            failureListContainer.style.display = 'none'; // Hide the failure section
        }
    }

    async function sendSummaries() {
        showView(processingView);

        try {
            const response = await fetch(`${backendUrl}/send-summaries`, {
                method: 'POST'
            });
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.message || 'An unknown error occurred.');
            }
            
            // Update the main success message
            completionMessage.textContent = `🎉 Process Complete! Summaries sent to ${result.data.sent_to.length} of ${result.data.total_processed} employees.`;
            
            // Call the new function to display the lists of names
            displaySummaryResults(result.data);
            showView(completionView);

        } catch (error) {
            console.error("Error sending summaries:", error);
            completionMessage.textContent = `❌ An error occurred: ${error.message}`;
            showView(completionView);
        }
    }

    startButton.addEventListener('click', sendSummaries);
});