    document.getElementById("register-form").addEventListener("submit", function (event) {
    let isValid = true;

    // Validate Student Number
    const studentNumber = document.getElementById("student_number");
    const studentNumberError = document.getElementById("student-number-error");
    if (studentNumber.value.trim() === "") {
        studentNumber.classList.add("invalid");
        studentNumberError.textContent = "Student number is required.";
        studentNumberError.style.display = "block";
        isValid = false;
    } else {
        studentNumber.classList.remove("invalid");
        studentNumberError.textContent = "";
        studentNumberError.style.display = "none";
    }

    // Validate Name
    const name = document.getElementById("name");
    const nameError = document.getElementById("name-error");
    if (name.value.trim() === "") {
        name.classList.add("invalid");
        nameError.textContent = "Name is required.";
        nameError.style.display = "block";
        isValid = false;
    } else {
        name.classList.remove("invalid");
        nameError.textContent = "";
        nameError.style.display = "none";
    }

    // Validate Email
    const email = document.getElementById("email");
    const emailError = document.getElementById("email-error");
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.value.trim())) {
        email.classList.add("invalid");
        emailError.textContent = "Enter a valid email address.";
        emailError.style.display = "block";
        isValid = false;
    } else {
        email.classList.remove("invalid");
        emailError.textContent = "";
        emailError.style.display = "none";
    }

    // Validate Password
    const password = document.getElementById("password");
    const passwordError = document.getElementById("password-error");
    if (password.value.trim() === "") {
        password.classList.add("invalid");
        passwordError.textContent = "Password is required.";
        passwordError.style.display = "block";
        isValid = false;
    } else {
        password.classList.remove("invalid");
        passwordError.textContent = "";
        passwordError.style.display = "none";
    }

    if (!isValid) {
        event.preventDefault(); // Prevent form submission if validation fails
    }
    });