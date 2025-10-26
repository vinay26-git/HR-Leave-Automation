document.addEventListener('DOMContentLoaded', () => {
    // Security check: if user is not logged in, redirect
    const username = sessionStorage.getItem('username');
    if (!username) {
        window.location.href = 'login.html';
        return;
    }
    
    // --- Configuration ---
    const HR_EMAIL = "revathinani22@gmail.com"; // Set your HR department's email here
    // --- End Configuration ---

    // Initialize the calendars
    const fullDayPicker = flatpickr("#full-day-picker", {
        mode: "multiple",
        dateFormat: "d-m-Y", // Set display format
        minDate: "today"
    });

    const halfDayPicker = flatpickr("#half-day-picker", {
        mode: "multiple",
        dateFormat: "d-m-Y", // Set display format
        minDate: "today"
    });

    const wfhPicker = flatpickr("#wfh-picker", {
        mode: "multiple",
        dateFormat: "d-m-Y", // Set display format
        minDate: "today"
    });

    const sendButton = document.getElementById('send-leave-request');
    const reasonInput = document.getElementById('leave-reason');

    // MODIFICATION: Helper function to format dates as DD-MM-YYYY
    function formatDate(dateObj) {
        const day = String(dateObj.getDate()).padStart(2, '0');
        const month = String(dateObj.getMonth() + 1).padStart(2, '0'); // Month is 0-indexed
        const year = dateObj.getFullYear();
        return `${day}-${month}-${year}`;
    }

    sendButton.addEventListener('click', () => {
        // MODIFICATION: Get the reason from the new input field
        const reason = reasonInput.value.trim();

        // Get the selected dates from each calendar and format them
        const fullDays = fullDayPicker.selectedDates.map(date => formatDate(date));
        const halfDays = halfDayPicker.selectedDates.map(date => formatDate(date));
        const wfhDays = wfhPicker.selectedDates.map(date => formatDate(date));
        
        // --- MODIFICATION: Add validation for the reason field ---
        if (!reason) {
            alert("Please provide a reason for your leave.");
            reasonInput.focus(); // Focus on the reason input
            return;
        }

        if (fullDays.length === 0 && halfDays.length === 0 && wfhDays.length === 0) {
            alert("Please select at least one date before sending.");
            return;
        }
        
        // --- MODIFICATION: Build the new email body with the reason ---
        let emailBody = `Hello HR Team,\n\nI would like to request the following time off for the reason: ${reason}\n\n`;
        
        if (fullDays.length > 0) {
            emailBody += `Full Day Leave(s):\n${fullDays.map(d => `- ${d}`).join('\n')}\n\n`;
        }
        if (halfDays.length > 0) {
            emailBody += `Half Day Leave(s):\n${halfDays.map(d => `- ${d}`).join('\n')}\n\n`;
        }
        if (wfhDays.length > 0) {
            emailBody += `Work From Home Day(s):\n${wfhDays.map(d => `- ${d}`).join('\n')}\n\n`;
        }

        const employeeName = sessionStorage.getItem('username') || 'Employee';
        emailBody += `Thank you,\n${employeeName}`;

        // --- MODIFICATION: Build the new email subject with the reason ---
        const subject = `Leave Request - ${reason}`;
        
        const gmailLink = `https://mail.google.com/mail/?view=cm&fs=1&to=${HR_EMAIL}&su=${encodeURIComponent(subject)}&body=${encodeURIComponent(emailBody)}`;

        window.open(gmailLink, '_blank');
    });
});