// Function to dynamically load content into the #content div
function loadContent(endpoint) {
    fetch(endpoint)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Failed to load content from ${endpoint}.`);
            }
            return response.text();
        })
        .then((html) => {
            const contentDiv = document.getElementById("content");
            if (!contentDiv) {
                throw new Error("Content div not found.");
            }

            // Update the page content
            contentDiv.innerHTML = html;

            // Dispatch a custom event to signal content has loaded
            document.dispatchEvent(new Event("contentloaded"));
        })
        .catch((error) => {
            console.error("Error loading content:", error);
            const contentDiv = document.getElementById("content");
            if (contentDiv) {
                contentDiv.innerHTML = `<p style="color: red;">Error loading content: ${error.message}</p>`;
            }
        });
}

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

// Attach listeners to dynamically loaded forms
function attachListeners() {
    // Handle Generate Plan form
    const generatePlanForm = document.getElementById("generate-plan-form");
    if (generatePlanForm) {
        console.log("Attaching listener to generate-plan-form.");
        generatePlanForm.addEventListener("submit", function (e) {
            e.preventDefault(); // Prevent default behavior
            const formData = new FormData(generatePlanForm);

            fetch("/generate-plan", {
                method: "POST",
                body: formData,
            })
                .then(response => {
                    if (!response.ok) throw new Error("Failed to generate plan");
                    return response.text();
                })
                .then(html => {
                    document.getElementById("generated-plan-results").innerHTML = html;
                })
                .catch(error => {
                    console.error("Error:", error);
                    document.getElementById("generated-plan-results").innerHTML = "<p>Error generating plan.</p>";
                });
        });
    } else {
        console.warn("generate-plan-form not found. No event listener attached.");
    }

    // Handle Update Form (if dynamically loaded)
    const updateForm = document.getElementById("update-form");
    if (updateForm) {
        console.log("Attaching listener to update-form.");
        updateForm.addEventListener("submit", (e) => {
            e.preventDefault();
            console.log("Update form submission intercepted.");

            const formData = new FormData(updateForm);

            fetch("/load-partial/student_info", {
                method: "POST",
                body: formData,
            })
                .then((response) => {
                    console.log("Response status:", response.status);
                    if (!response.ok) {
                        throw new Error("Failed to update information.");
                    }
                    return response.text();
                })
                .then((updatedHtml) => {
                    console.log("Updated HTML received.");
                    document.getElementById("content").innerHTML = updatedHtml; // Update content dynamically
                })
                .catch((error) => {
                    console.error("Error updating information:", error);
                    document.getElementById("content").innerHTML =
                        "<p style='color: red;'>Error updating information.</p>";
                });
        });
    } else {
        console.warn("update-form not found. No event listener attached.");
    }
}

// Listen for the custom "contentloaded" event to attach listeners to newly loaded content
document.addEventListener("contentloaded", attachListeners);

// Initial setup when DOM content is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    console.log("Page loaded. Attaching event listeners.");
    attachListeners();
});

// Function to load the Generate Plan page
function loadGeneratePlan() {
    loadContent('/load-partial/generated_plan');
}

// Toggle the navbar visibility
function toggleNavbar() {
    const navbar = document.getElementById("navbar");
    const content = document.getElementById("content");

    if (navbar.classList.contains("collapsed")) {
        navbar.classList.remove("collapsed");
        content.style.marginLeft = "270px";
    } else {
        navbar.classList.add("collapsed");
        content.style.marginLeft = "70px";
    }
}

// Function to fetch the study plan data
function getStudyPlanData() {
    const rows = document.querySelectorAll(".study-plan-container table tbody tr");
    const data = [];

    rows.forEach((row) => {
        const cells = row.querySelectorAll("td");
        const rowData = Array.from(cells).map(cell => cell.textContent.trim());
        data.push(rowData);
    });

    return data;
}

// Function to export the study plan
function exportStudyPlan(format) {
    console.log("Exporting study plan as:", format);
    const planData = getStudyPlanData(); // Fetch study plan data
    console.log("Study Plan Data:", planData);

    fetch(`/export-plan/${format}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            plan: planData,
            plan_type: "study_plan" // Add plan type
        })
    })
    .then(response => {
        if (!response.ok) throw new Error(`Failed to export ${format} file.`);
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `study_plan.${format}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    })
    .catch(error => console.error("Error exporting study plan:", error));
}

// Function to fetch the generated plan data
function getGeneratedPlanData() {
    const rows = document.querySelectorAll("#generated-plan-results table tbody tr");
    const data = [];

    rows.forEach((row) => {
        const cells = row.querySelectorAll("td");
        const rowData = Array.from(cells).map(cell => cell.textContent.trim());
        data.push(rowData);
    });

    return data;
}

// Function to export the generated plan
function exportGeneratedPlan(format) {
    console.log("Exporting generated plan as:", format);
    const planData = getGeneratedPlanData(); // Fetch generated plan data
    console.log("Generated Plan Data:", planData);

    fetch(`/export-plan/${format}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            plan: planData,
            plan_type: "generated_plan" // Add plan type
        })
    })
    .then(response => {
        if (!response.ok) throw new Error(`Failed to export ${format} file.`);
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `generated_plan.${format}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    })
    .catch(error => console.error("Error exporting generated plan:", error));
}

