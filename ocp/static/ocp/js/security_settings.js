/*
    Created By : Christian Merriman
    Function: Used for the security settings to change users access levels
*/

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('personnelSearch');
    const tableRows = document.querySelectorAll('.personnel-row');

    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchTerm = searchInput.value.toLowerCase();

            tableRows.forEach(row => {
                // Search by Username (Identifier)
                const username = row.querySelector('.username').textContent.toLowerCase();
                // Also allow search by Employee ID
                const employeeId = row.querySelector('.tech-id').textContent.toLowerCase();

                if (username.includes(searchTerm) || employeeId.includes(searchTerm)) {
                    row.style.display = ""; // Show row
                } else {
                    row.style.display = "none"; // Hide row
                }
            });
        });
    }
});