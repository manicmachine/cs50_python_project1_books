var email = document.getElementById('email'),
    emailConfirmation = document.getElementById('emailConfirmation'),
    password = document.getElementById("password"),
    passwordConfirmation = document.getElementById("passwordConfirmation");

function validateEmail() {
    if(email.value != emailConfirmation.value) {
        emailConfirmation.setCustomValidity("Emails don't match");
    } else {
        emailConfirmation.setCustomValidity("");
    }
}

function validatePassword() {
    if(password.value != passwordConfirmation.value) {
        passwordConfirmation.setCustomValidity("Passwords don't match");
    } else {
        passwordConfirmation.setCustomValidity("");
    }
}

email.onchange = validateEmail;
emailConfirmation.onkeyup = validateEmail;
password.onchange = validatePassword;
passwordConfirmation.onkeyup = validatePassword;