console.log("generate_plan.js loaded successfully");
const generatePlanForm = document.getElementById("generate-plan-form");
if (generatePlanForm) {
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
}

