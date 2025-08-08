
// Real-time Validation
document.getElementById("update-form").addEventListener("input", (e) => {
    const target = e.target;

    // Name validation
    if (target.id === "name") {
        const error = document.getElementById("name-error");
        error.textContent = target.value.trim() === "" ? "Name is required" : "";
    }

    // Email validation
    if (target.id === "email") {
        const error = document.getElementById("email-error");
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        error.textContent = emailRegex.test(target.value)
            ? ""
            : "Please enter a valid email address";
    }

    // Phone validation
    if (target.id === "phone") {
        const error = document.getElementById("phone-error");
        const phoneRegex = /^\+?[0-9]{10,15}$/;
        error.textContent = phoneRegex.test(target.value)
            ? ""
            : "Enter a valid phone number (e.g., +1234567890)";
    }
});

const updateForm = document.getElementById("update-form");
if (updateForm) {
    updateForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const formData = new FormData(updateForm);

        fetch("/load-partial/student_info", {
            method: "POST",
            body: formData,
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Failed to update information.");
            }
            return response.text();
        })
        .then((updatedHtml) => {
            document.getElementById("content").innerHTML = updatedHtml;
        })
        .catch((error) => {
            console.error("Error updating information:", error);
            document.getElementById("content").innerHTML =
                "<p style='color: red;'>Error updating information.</p>";
        });
    });
}
