console.log("generate_plan.js loaded successfully");
// Add event listener to toggle row background color on checkbox click
document.querySelectorAll('.checkbox').forEach((checkbox) => {
    checkbox.addEventListener('change', function () {
        const row = this.closest('tr'); // Find the closest table row
        if (this.checked) {
            row.classList.add('completed'); // Add the "completed" class
        } else {
            row.classList.remove('completed'); // Remove the "completed" class
        }
    });

    // Ensure initial state is applied
    if (checkbox.checked) {
        checkbox.closest('tr').classList.add('completed');
    }
});

// Function to save the study plan
function saveStudyPlan() {
    const checkboxes = document.querySelectorAll('input[name="completed_courses"]:checked');
    const completedCourses = Array.from(checkboxes).map(cb => cb.value);

    fetch('/save-study-plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ completed_courses: completedCourses })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Study plan saved successfully!');
        } else {
            alert('Failed to save study plan.');
        }
    })
    .catch(error => {
        console.error('Error saving study plan:', error);
        alert('An error occurred.');
    });
}

