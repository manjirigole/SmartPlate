function validateForm() {
    var password = document.getElementById("password").value;
    var passwordError = document.getElementById("password-error");

    // Regular expression to check for at least 8 characters including special characters
    var passwordRegex = /^(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$/;

    // Check if password meets criteria
    if (!passwordRegex.test(password)) {
        passwordError.innerText = "Password must be at least 8 characters long and contain special characters";
        alert("Password must be at least 8 characters long and contain special characters"); // Display alert box
        return false; // Prevent form submission
    }

    // If password is valid, clear any previous error message
    passwordError.innerText = "";
    return true; // Allow form submission
}
